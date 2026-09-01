from computers.pc import PC
from computers.laptop import Laptop
from computers.server import Server


def create_objects():
    devices = []

    # 10 PC objects
    pc_cpus = [
        "Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9", "AMD Ryzen 3",
        "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9", "Intel Core i5-13400", "AMD Ryzen 5 5600X"
    ]
    for i in range(10):
        pc = PC(
            cpu=pc_cpus[i],
            ram=8 + (i % 4) * 8,
            storage=256 + (i * 256),
            form_factor="Mini-ITX" if i % 2 == 0 else "ATX"
        )
        devices.append(pc)

    # 10 Laptop objects
    laptop_cpus = [
        "Apple M1", "Apple M2", "Apple M3", "Intel Core i5-1240P", "Intel Core i7-12700H",
        "AMD Ryzen 7 6800U", "Intel Core Ultra 7", "AMD Ryzen 9 7940HS", "Apple M2 Pro", "Apple M3 Max"
    ]
    for i in range(10):
        laptop = Laptop(
            cpu=laptop_cpus[i],
            ram=8 + (i % 3) * 8,
            storage=512 + (i % 4) * 512,
            battery_life=6 + i
        )
        devices.append(laptop)

    # 10 Server objects
    server_cpus = [
        "AMD EPYC 7763", "AMD EPYC 9654", "Intel Xeon Silver 4314", "Intel Xeon Gold 6330", "Intel Xeon Platinum 8380",
        "AMD EPYC 7543", "Intel Xeon E-2388G", "AMD EPYC 9354", "Intel Xeon Gold 5418Y", "AMD EPYC 7713"
    ]
    for i in range(10):
        server = Server(
            cpu=server_cpus[i],
            ram=32 + i * 32,
            storage=1000 + i * 2000,
            rack_units=1 + (i % 4)
        )
        devices.append(server)

    return devices


def main():
    devices = create_objects()

    print(f"Total objects created: {len(devices)}\n")
    print("=" * 85)
    print(f"{'№':<3} | {'Class':<8} | {'CPU (ЦП)':<22} | {'RAM (ОЗУ)':<10} | {'Storage (Память)':<16} | {'Extra Param'}")
    print("=" * 85)

    for idx, dev in enumerate(devices, 1):
        cpu = dev.get_parameter("cpu")
        ram = f"{dev.get_parameter('ram')} GB"
        storage = f"{dev.get_parameter('storage')} GB"

        extra = ""
        if isinstance(dev, PC):
            extra = f"Form: {dev.get_parameter('form_factor')}"
        elif isinstance(dev, Laptop):
            extra = f"Battery: {dev.get_parameter('battery_life')}h"
        elif isinstance(dev, Server):
            extra = f"Rack: {dev.get_parameter('rack_units')}U"

        print(f"{idx:<3} | {dev.__class__.__name__:<8} | {cpu:<22} | {ram:<10} | {storage:<16} | {extra}")

    print("=" * 85)

    # Demonstration of set_parameter and get_parameter interface methods
    print("\nDemonstration of set_parameter and get_parameter interface methods on object #1:")
    sample_dev = devices[0]
    print(f"Before modification: {sample_dev}")
    sample_dev.set_parameter("ram", 64)
    sample_dev.set_parameter("cpu", "Intel Core i9-13900K")
    print(f"After set_parameter('ram', 64) & set_parameter('cpu', ...): {sample_dev}")
    print(f"Getting parameter 'cpu': {sample_dev.get_parameter('cpu')}")
    print(f"Getting parameter 'ram': {sample_dev.get_parameter('ram')}")


if __name__ == "__main__":
    main()

