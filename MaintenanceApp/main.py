from vinDecoder import decode_vin

def main():
    test_vin = "1HGCM82633A004352"
    vehicle = decode_vin(test_vin)

    if vehicle:
        print("Decoded Vehicle Info:")
        print(vehicle.to_dict())
    else:
        print("Failed to decode VIN.")

if __name__ == "__main__":
    main()
