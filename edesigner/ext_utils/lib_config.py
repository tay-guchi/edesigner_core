class DesignConfig:
    def __init__(self, block):
        self.block = block
        lines = self.block.split("\n")
        self.design_id = lines[1].split(" ")[-1]
        self.scope = lines[3].split(" ")[-1].split(".")[-1]
        self.size = lines[4].split(" ")[-1]
        self.num_cycle = lines[5].split(" ")[-1]
        reaction_list = []
        for line in lines:
            if line.startswith("START:"):
                self.hp = line.split(" ")[1]
                
            elif line.find("||file=") > 0:
                if line.find("_C1") > 0:
                    self.c1 = line.split("||")[0].split("/")[-1]
                    
                elif line.find("_C2") > 0:
                    self.c2 = line.split("||")[0].split("/")[-1]
                    
                elif line.find("_C3") > 0:
                    self.c3 = line.split("||")[0].split("/")[-1]
                    
                reaction_list.append(line.split("||")[0].split("/")[-1])
                
            elif line.startswith("/home"):
                reaction_list.append(line.split("/")[-1])
                
        self.reaction_list = reaction_list
        
        
    def print_config(self):
        print(f"Design ID: { self.design_id}")
        print(f"Library size: {self.size}")
        print(f"Number of cycles: {self.num_cycle}\n")
        print(f"Headpiece: {self.hp}")
        print(f"Cycle1 reaction: {self.c1}")
        print(f"Cycle2 reaction: {self.c2}")
        print(f"Cycle3 reaction: {self.c3}\n")
        
        print("Reaction Sequence including deprotection")
        print("\n".join(self.reaction_list))
        
        
    def modify_config(self):
        new_block = ""
        lines = self.block.split("\n")
        for line in lines:
            if line.find("X.X.X_Aminothiazole_synthesis_FROM_amines_aliphatic_primary_AND_a_h_ketones.rxn") > 0:
                line += "||\n"
            elif line.find("X.X.X_Aminothiazole_synthesis_FROM_amines_aliphatic_primary_AND_ketones_a_bromo") > 0:
                line += "||\n"
            elif line.find("9.7.8_Amino_to_guanidino_FROM_amines_aliphatic_AND_amines_aliphatic.rxn") > 0:
                line += "||\n"
            elif line.find("4.2.2_1,2,4-Oxadiazole_synthesis_FROM_amines_aliphatic_primary_AND_carboxylic_acids.rxn") > 0:
                line += "||\n"
            elif line.find("4.2.17_1,3-Benzoxazole_synthesis_FROM_amines_aliphatic_primary_AND_o_amino_phenols.rxn") > 0:
                line += "||\n"
            else:
                line += "\n"
                
            new_block += line
            
        self.block = new_block
        
        
    def write_config(self, filename):
        basename = filename.replace("_config.txt", "")
        if self.scope == "INTERNAL":
            fname = f"{basename}_{str(self.design_id)}_int_config.txt"
        else:
            fname = f"{basename}_{str(self.design_id)}_config.txt"
            
        with open(fname, "w") as out:
            out.write(self.block)
            
