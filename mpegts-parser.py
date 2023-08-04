import os
import sys
import argparse
from bitstring import BitStream

def parse_ts_file(file_path):
    ts_packet_size = 188 
    
    with open(file_path, 'rb') as file:
        packet_count = 0
        pids = []
        while True:
            packet_data = file.read(ts_packet_size)
            if not packet_data: # No more packets to read
                sorted_pids = sorted(pids, key=lambda x: int(x, 16))
                for pid in sorted_pids:
                    print(pid)
                sys.exit(0) # Exit with Success Code

            packet = BitStream(packet_data)

            sync_byte = packet_data[0] # Takes first byte (Sync Byte)

            if sync_byte != 0x47:
                offset = packet_count * ts_packet_size
                print("Error: No sync byte present in packet " + str(packet_count) + ", offset " + str(offset))
                sys.exit(1) # Exit with error code

            second_byte = packet_data[1]
            third_byte = packet_data[2]

            pid_part_a = second_byte & 0x1F
            pid = ((pid_part_a << 8) | third_byte) & 0x1FFF # Ensures that PIDs are combined formatted correctly
            pid_hex = "0x{:X}".format(pid)

            if pid_hex not in pids: # Ensures only unique values are stored
                pids.append(pid_hex)

            packet_count += 1    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    
    file_path = args.file_path
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    parse_ts_file(file_path)

if __name__ == "__main__":
    main()
