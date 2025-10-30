from tabulate import tabulate

class Interface:
    """
    Responsável por toda a exibição textual (saída) e coleta
    de dados (entrada) da simulação.
    """

    def __init__(self):
        """
        Inicializa a interface.
        """
        self.step_by_step = False

    def set_demo_mode(self, enable):
        """
        Ativa ou desativa o modo de demonstração (passo a passo).
        """
        if enable:# Ativa diretamente
            self.step_by_step = True 
            print("Modo demonstração (passo a passo) ativado.")
        else: # Pergunta ao usuário
            choice = input("Deseja ativar o modo demonstração (passo a passo)? (s/n): ").strip().lower()
            if choice == 's':
                self.step_by_step = True
                print("Modo demonstração (passo a passo) ativado.")

    def display_step(self, state_data):
        """
        Exibe o estado da simulação após um acesso.
        
        Args:
            state_data (dict): Dicionário vindo de simulator.get_simulation_state()
        """
        print("\n" + "=" * 60)
        print(" ESTADO ATUAL DA SIMULAÇÃO")
        print("=" * 60)
        if self.step_by_step: # verifica se está no modo passo a passo
            page_headers = ["Página Virtual", "Moldura Física", "Bit de Presença"]
            data_table_pages = []
            page_table_entries = state_data['page_table']
            for entry in page_table_entries:
                if entry.present:
                    frame_display = entry.frame_number
                else:
                    frame_display = "---" # Mostra "---" se não estiver na memória
                
                data_table_pages.append([
                    entry.page_number, 
                    frame_display, 
                    entry.present
                ])
            print(tabulate(data_table_pages, headers=page_headers, tablefmt="grid", stralign="center"))
            
            input("  Pressione Enter para o próximo acesso...")
            print("\n" + "=" * 60)
    
    def display_final_report(self, report_data):
        """
        Exibe o relatório final da simulação de forma organizada
        usando a biblioteca 'tabulate'.

        Args:
            report_data (dict): Dicionário vindo de simulator.get_final_report()
        """
        print("\n" + "=" * 60)
        print("RELATÓRIO FINAL DA SIMULAÇÃO")
        print("=" * 60)

        total_faults = report_data['total_page_faults']
        print(f"\nTotal de Falhas de Página: {total_faults}\n")

        print("--- Tabela de Páginas (Estado Final) ---")
        
        page_headers = ["Página Virtual", "Moldura Física", "Bit de Presença"]
        data_table_pages = []
        
        page_table_entries = report_data['page_table_entries']
        
        # Transforma os objetos em listas para o tabulate
        for entry in page_table_entries:
            # Formata a moldura para ficar mais legível
            if entry.present:
                frame_display = entry.frame_number
            else:
                frame_display = "---" # Mostra "---" se não estiver na memória
            
            data_table_pages.append([
                entry.page_number, 
                frame_display, 
                entry.present
            ])
        
        # Imprime a tabela formatada
        print(tabulate(data_table_pages, headers=page_headers, tablefmt="grid", stralign="center"))

        print("\n--- Memória Física (Estado Final) ---")
        
        # Cabeçalhos da tabela
        memory_headers = ["Moldura (Frame)", "Conteúdo (Página)"]
        physical_memory_data = []

        # Pega a lista de molduras (ex: [0, 1, 4, 2])
        physical_memory_frames = report_data['physical_memory_frames']

        # Transforma a lista em dados para o tabulate
        for frame_num, page_num in enumerate(physical_memory_frames):
            if page_num == -1:
                content = "(Vazio)"
            else:
                content = f"Página {page_num}"
            
            physical_memory_data.append([frame_num, content])
            
        # Imprime a tabela formatada
        print(tabulate(physical_memory_data, headers=memory_headers, tablefmt="grid", stralign="center"))
        print("=" * 60)

    def get_inputs(self):
        """
        Coleta as entradas do usuário (Tamanhos de memória e lista de acessos).
        
        Retorna:
            tuple: (num_frames, num_pages, access_list)
        """
        
        choice = input("Deseja inserir os dados manualmente? (s/n): ").strip().lower()
        if choice == 's':
            num_frames = int(input("Número de molduras na memória física: "))
            num_pages = int(input("Número de páginas na memória virtual: "))
            access_list_input = input("Lista de acessos (páginas separadas por espaço): ")
            access_list = access_list_input.split()
            return num_frames, num_pages, access_list
        else:
            print("Usando as entradas padrão.")
        
            # Valores provisórios para permitir a execução 
            num_frames = 4
            num_pages = 8
            access_list = "0 1 2 3 0 1 4 0 1 2 3 4".split()
        
        return num_frames, num_pages, access_list