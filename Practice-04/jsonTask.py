import json


def safe_get(a, key, default=""):
    b = a.get(key, default)
    return "" if b is None else str(b)

def main():
    with open("sample-data.json", 'r') as f:
        data = json.load(f)

    rows = []

    for item in data.get("imdata", []):
        attrs = item.get('l1PhysIf', {}).get('attributes', {})
        rows.append({"dn": safe_get(attrs, "dn"),
                     "descr": safe_get(attrs, "descrt"),
                     "speed": safe_get(attrs, "speed"),
                     "mtu": safe_get(attrs, "mtu")})
    
    dn_width, descr_width, speed_width, mtu_width = 62, 26, 8, 6

    print("Interface Status")
    print("=" * (dn_width + 1 + descr_width + 1 + speed_width + 1 + mtu_width))
    print(f"{'DN':<{dn_width}} {'Description':<{descr_width}} {'Speed':<{speed_width}} {'MTU':<{mtu_width}}")
    print(f"{'-' * dn_width} {'-' * descr_width} {'-' * speed_width} {'-' * mtu_width}")

    for i in rows:
        dn = (i["dn"][:dn_width-1] + "…") if len(i["dn"]) > dn_width else i["dn"]
        descr = (i["descr"][:descr_width-1] + "…") if len(i["descr"]) > descr_width else i["descr"]

        print(f"{dn:<{dn_width}} {descr:<{descr_width}} {i['speed']:<{speed_width}} {i['mtu']:<{mtu_width}}")


if __name__ == "__main__":
    main()