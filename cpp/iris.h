#ifndef IRIS_H
#define IRIS_H

#include <stdint.h>

/***** Example *****

// Notice that endianess of the target processor is defined with -D option of the compiler in this example.

#include "iris.h"                 // *** for IrisSender & MessageId
using namespace iris;             // *** working with objets from iris namespace

#include <iostream>               // *** for std::cout

void sendchar(uint8_t c) {        // *** function for sending bytes
	std::cout << c;               // *** we just print the byte on stdout
}

int main() {                      // *** here is the main
	IrisSender comm(sendchar);    // *** we create a IrisSender objet with the previous sending function
	                              //     In our case, we can use directly `putchar` but I wanted to show
								  //     you how to deal with custom sending functions
	comm << MessageId(0x64);      // *** The first thing is to send the message ID, here 0x64
	comm << 1.0f;                 // *** Now we send data (`backabackbsd` encoder is used)
	comm << 1.0f << 1.0f << 2.0f; // *** We can chain data like this
	comm << endmsg;               // *** Finally, we send the `endmsg` object in order to actually send 
	                              //     the calculated checksum. Be aware to send ID _and_ endmsg as 
								  //     well as data !
}

***** End of example *****/
 
namespace iris {

	enum MessageId {};

	class MessageEnd {};
	extern MessageEnd endmsg;
	
	typedef uint16_t (*ChecksumFct) (int16_t sum, uint8_t data);
	typedef void (*SendFct) (uint8_t data);
	
	inline uint16_t bsd_checksum(uint16_t sum, uint8_t data) {
		if (sum & 1) sum = (sum >> 1) + 0x8000;
		else sum = (sum >> 1);
		sum += data;
		return sum;
	}
	
	class IrisSender {
		public:
			IrisSender(SendFct sendfct, ChecksumFct cksfct = (ChecksumFct) &bsd_checksum) : send(sendfct), checksum_update(cksfct) {}
			#if defined(LITTLE_ENDIAN)
			template <typename type> IrisSender & operator << (const type data) {
				const uint8_t * ptr = (uint8_t *) &data + sizeof(type);
				while (ptr != (uint8_t *) &data) operator << (*--ptr);
				return *this;
			}
			#else
			#if defined(BIG_ENDIAN)
			template <typename type> IrisSender & operator << (const type data) {
				uint8_t cnt = sizeof(type) + 1;
				const uint8_t * ptr = (uint8_t *) &data - 1;
				while (--cnt) operator << (*++ptr);
				return *this;
			}
			#else
			#error No endianess defined
			#endif
			#endif
			IrisSender & operator << (const uint8_t data) {
				checksum = checksum_update(checksum, data);
				send(data);
				return *this;
			}
			IrisSender & operator << (const MessageId id) {
				checksum = 0;
				return operator << ((uint8_t) id);
			}
			IrisSender & operator << (const MessageEnd) {
				uint8_t checksum_lsb = checksum;
				operator << ((uint8_t)(checksum >> 8));
				return operator << ((uint8_t) checksum_lsb);
			}

		private:
			uint16_t checksum;
			const SendFct send;
			const ChecksumFct checksum_update;
	};
}
 
 #endif
