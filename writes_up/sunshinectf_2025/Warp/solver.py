from bcc import BPF
import ctypes as ct
import time
import os

# Define the eBPF program
bpf_text = """
#include <uapi/linux/bpf.h>

BPF_RINGBUF_OUTPUT(rb, 1);

int hello(void *ctx) {
    char msg[] = "Hello, World!";
    rb.ringbuf_output(msg, sizeof(msg), 0);
    return 0;
}
"""

# Load the eBPF program
b = BPF(text=bpf_text)

# Keep the script running to keep the map alive
print("BPF map 'rb' created. Keeping it alive...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting.")
