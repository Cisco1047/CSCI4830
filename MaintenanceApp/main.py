from vinDecoder import decode_vin

def main():
    test_vin = "3VW267AJ5GM371022"
    vehicle = decode_vin(test_vin)

    print('test')

    if vehicle:
        print("Decoded Vehicle Info:")
        print(vehicle.to_dict())
    else:
        print("Failed to decode VIN.")

if __name__ == "__main__":
    main()
