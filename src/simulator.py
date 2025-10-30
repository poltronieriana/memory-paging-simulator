from collections import deque
from memory import PageTable, PhysicalMemory

class Simulator:
    """
    Gerencia a lógica principal da simulação, incluindo o tratamento
    de acessos a páginas e a aplicação do algoritmo de substituição.
    """

    def __init__(self, num_frames, num_pages):
        """
        Inicializa o simulador com as estruturas de memória.
        
        Args:
            num_frames (int): Número de molduras na memória física.
            num_pages (int): Número de páginas na memória virtual.
        """
        self.page_table = PageTable(num_pages)
        self.physical_memory = PhysicalMemory(num_frames)
        self.page_faults = 0
        self.num_frames = num_frames
        
        # Estrutura de dados pro FIFO
        self.fifo_queue = deque()

        self.last_acess_was_fault = False
        
        # Funções de callback para a interface (vão ser injetadas)
        self.display_callback = None
        self.report_callback = None

    def set_display_callbacks(self, display_step, display_report):
        """
        Registra as funções da interface que devem ser chamadas
        durante e ao final da simulação.
        """
        self.display_callback = display_step
        self.report_callback = display_report

    def run(self, virtual_access_list):
        """
        Executa o loop principal da simulação, processando
        cada acesso da lista.
        """
        print(f"[Simulator] Iniciando simulação...")
        
        for virtual_address in virtual_access_list:
            
            page_number = self.translate_address(virtual_address)
            
            if page_number is None or page_number >= len(self.page_table.entries):
                print(f"[Simulator] Erro: Endereço virtual {virtual_address} inválido.")
                continue

            # Processa o acesso à página
            self.access_page(page_number)
            
            # Chama o callback da interface para mostrar o estado
            if self.display_callback:
                # Prepara os dados para a interface
                state = self.get_simulation_state(page_number)
                self.display_callback(state)

        # Chama o callback de relatório final (I4)
        if self.report_callback:
            final_report = self.get_final_report()
            self.report_callback(final_report)

    def access_page(self, page_number):
        """
        Processa um acesso a uma página virtual.
        Deve verificar se a página está presente (hit) ou não (fault).
        """

        self.last_acess_was_fault = False

        # 1. verficação (hit ou fault)
        if self.page_table.is_present(page_number):
            # Página está na memória (hit)
            print(f"Página {page_number} acessada com sucesso. (HIT)")

        else:
            # Página não está na memória (fault)
            print(f"Página {page_number} não está na memória. (FAULT)")
            self.page_faults += 1 # Incrementa contador de falhas
            
            self.last_acess_was_fault = True  

            # Chama o tratamento de falha de página
            self.handle_page_fault(page_number)


    def handle_page_fault(self, page_number):
        """
        Trata uma falha de página.
        Deve encontrar uma moldura livre ou aplicar o FIFO se a memória estiver cheia.
        """
        free_frame =-1
        # tenta encontrar uma moldura livre
        try:
            # O PhysicalMemory.frames armazena a página (int) ou -1 (livre
            free_frame = self.physical_memory.frames.index(-1)
            print(f"Moldura livre encontrada: {free_frame}")

        # se não tiver moldura livre, aplica o FIFO
        except ValueError:
            print("Memória cheia. Aplicando FIFO para substituição.")

            # Remove a página mais antiga da fila FIFO
            page_to_remove = self.fifo_queue.popleft()  

            # Encontra a moldura da página a página antiga tava usando
            frame_to_free = self.page_table.get_frame(page_to_remove)

            # Atualiza a tabela de páginas e memória física
            self.physical_memory.free_frame(frame_to_free)
            self.page_table.remove_mapping(page_to_remove)

            free_frame = frame_to_free

        # Carrega a nova página na moldura livre
        self.load_page(page_number, free_frame)

    def load_page(self, page_number, frame_number):
        """
        Função auxiliar para carregar uma página em uma moldura.
        Atualiza memória, tabela e fila.
        (Implementação de I2)
        """
        self.physical_memory.allocate_frame(frame_number, page_number)

        self.page_table.set_mapping(page_number, frame_number)

        # Adiciona a página carregada na fila FIFO
        self.fifo_queue.append(page_number)

        print(f"Página {page_number} carregada na moldura {frame_number}.")

    def translate_address(self, virtual_address):
        """
        Converte um endereço virtual em um número de página.
        """
        try:
            return int(virtual_address)
        except ValueError:
            return None

    def get_simulation_state(self, last_page_accessed):
        """
        Empacota o estado atual da simulação para a interface.
        Esta é uma função de integração (I3).
        
        Retorna:
            dict: Dicionário com o estado atual.
        """
        return {
            "page_table": self.page_table.entries,
            "physical_memory": self.physical_memory,
            "page_faults_count": self.page_faults,
            "last_accessed_page": last_page_accessed,
            "page_fault_occurred": self.last_acess_was_fault
        }

    def get_final_report(self):
        """
        Empacota o relatório final para a interface.
        Envia os dados brutos para a interface formatar.
        """
        return {
            "total_page_faults": self.page_faults,
            "page_table_entries": self.page_table.entries,       
            "physical_memory_frames": self.physical_memory.frames  
        }