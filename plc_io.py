from pylogix import PLC

def bitwise_write_sint(original_val: int, bit_index: int, bit_value: int):
    """Writes a single bit in an 8-bit SINT value."""
    if not 0 <= bit_index <= 7:
        raise ValueError("Bit index must be between 0 and 7.")
    if bit_value not in [0, 1]:
        raise ValueError("Bit value must be 0 or 1.")

    if bit_value == 1:
        return original_val | (1 << bit_index)
    else:
        return original_val & ~(1 << bit_index)

def parse_bit_tag(full_tag: str):
    """
    Converts a tag like 'RC4A0315:13:I.5' into:
    ('RC4A0315:I.Data[13]', 5)
    """
    try:
        module, rest = full_tag.split(":", 1)
        slot, direction_bit = rest.split(":", 1)
        direction, bit_str = direction_bit.split(".")
        bit_num = int(bit_str)
        tag_name = f"{module}:{direction}.Data[{slot}]"
        return tag_name, bit_num
    except Exception as e:
        raise ValueError(f"Invalid tag format: {full_tag}") from e

class PylogixPLC:
    def __init__(self, ip):
        self.ip = ip
        self.plc = PLC()
        self.plc.IPAddress = ip

    def read_tag(self, tag):
        """Reads a tag (bit or word)."""
        try:
            response = self.plc.Read(tag)
            if response.Status == 'Success':
                return response.Value
            print(f"[READ ERROR] {tag} -> {response.Status}")
            return False
        except Exception as e:
            print(f"[READ EXCEPTION] {tag} -> {e}")
            return False

    def write_tag(self, tag, value):
        """
        Writes to either a full tag or a digital bit tag (e.g., RC4A0315:13:I.5).
        Handles digital bit writes by reading, modifying, then writing the word.
        """
        try:
            if "." in tag and tag[-2] == "." and tag[-1].isdigit():
                # Probably a digital tag like RC4A0315:13:I.5
                return self.write_digital_bit(tag, value)
            else:
                result = self.plc.Write(tag, value)
                if result.Status == 'Success':
                    print(f"[PLC WRITE] {tag} = {value}")
                else:
                    print(f"[WRITE ERROR] {tag} = {value} -> {result.Status}")
        except Exception as e:
            print(f"[WRITE EXCEPTION] {tag} -> {e}")

    def write_digital_bit(self, bit_tag, bit_value):
        """
        Write a 0/1 to a digital bit tag like RC4A0315:13:I.5 by reading the SINT,
        modifying the bit, and writing the full word.
        """
        try:
            tag_name, bit = parse_bit_tag(bit_tag)
            current = self.plc.Read(tag_name)
            if current.Status != 'Success':
                print(f"[READ ERROR before write] {bit_tag} -> {current.Status}")
                return

            new_val = bitwise_write_sint(current.Value, bit, bit_value)
            result = self.plc.Write(tag_name, new_val)
            if result.Status == 'Success':
                print(f"[BIT WRITE] {bit_tag} = {bit_value} -> {tag_name} = {new_val}")
            else:
                print(f"[BIT WRITE ERROR] {bit_tag} -> {result.Status}")
        except Exception as e:
            print(f"[BIT WRITE EXCEPTION] {bit_tag} -> {e}")