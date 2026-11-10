import json

def load_knowledge_base(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_forward_chaining(kb):
    print(f"=== {kb['judul']} ===")
    print(f"Catatan: {kb['batas']}\n")
    print("Jawablah pertanyaan berikut dengan 'y' (ya) atau 't' (tidak).\n")
    
    base_facts = [
        "sudah menempuh minimal 115 SKS",
        "IPK minimal 2.00",
        "tidak ada nilai E",
        "lulus praktikum atau tugas besar",
        "lulus praktik kerja lapangan (PKL)",
        "similarity Turnitin maksimal 30 persen",
        "lulus seminar hasil",
        "sudah menempuh minimal 144 SKS",
        "lulus ujian pendadaran"
    ]
    
    rule_conclusions = {rule['maka'] for rule in kb['aturan']}
    
    memory = set()
    reasons = {}
    
    for fact in base_facts:
        answer = input(f"Apakah {fact}? (y/t) > ").strip().lower()
        if answer == 'y':
            memory.add(fact)
            reasons[fact] = "Fakta awal dari pengguna"
            
    print("\n--- Proses Inferensi (Forward Chaining) ---")
    iteration = 1
    
    fired_rules_order = []
    
    while True:
        rule_fired = False
        for rule in kb['aturan']:
            consequent = rule['maka']
            
            if consequent in memory:
                continue
                
            premises = rule['jika']
            mode = rule['mode']
            
            if mode == "dan":
                condition_met = all(p in memory for p in premises)
            elif mode == "atau":
                condition_met = any(p in memory for p in premises)
            else:
                condition_met = False
                
            if condition_met:
                memory.add(consequent)
                reasons[consequent] = {
                    "rule_id": rule['id'],
                    "premises": premises,
                    "sumber": rule['sumber']
                }
                fired_rules_order.append(consequent)
                print(f"Siklus {iteration}: {rule['id']} -> {consequent} (Sumber: {rule['sumber']})")
                rule_fired = True
                iteration += 1
                
        if not rule_fired:
            break
            
    print("\n================ HASIL KESIMPULAN ================")
    conclusions = [c for c in memory if c in rule_conclusions]
    
    rule_order_map = {rule['maka']: i for i, rule in enumerate(kb['aturan'])}
    conclusions.sort(key=lambda x: rule_order_map.get(x, 99))
    
    if not conclusions:
        print("Kesimpulan: Tidak ada kesimpulan yang dicapai (Kasus Negatif / Belum memenuhi syarat).")
    else:
        print(f"Kesimpulan utama yang dicapai:")
        for c in conclusions:
            print(f" - {c}")
            
        print("\nAlasan & Jejak Aturan (Chaining):")
        
        printed_items = set()
        def print_reason(item, indent=2):
            if item in reasons:
                detail = reasons[item]
                if detail == "Fakta awal dari pengguna":
                    if item not in printed_items:
                        printed_items.add(item)
                        print(" " * indent + f"- {item} <- [Fakta Pengguna]")
                else:
                    print(" " * indent + f"- {item} <- {detail['rule_id']} [Sumber: {detail['sumber']}]")
                    for p in detail['premises']:
                        print_reason(p, indent + 2)
                        
        for c in conclusions:
            print_reason(c)
            
    print(f"\nCatatan: {kb['batas']}")

if __name__ == "__main__":
    knowledge_base = load_knowledge_base("kb_kelayakan.json")
    run_forward_chaining(knowledge_base)