from collections import deque
from .memory import PageTable, PhysicalMemory

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
            
            # Chama o callback da interface (I4) para mostrar o estado
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
        # TODO: integrante 2 mexe aqui
        
        print(f"[Simulator Stub] Acessando página {page_number}. (Lógica de I2 pendente)")
        
        # Exemplo de lógica provisória mínima de falha (para testar a integração)
        if not self.page_table.is_present(page_number):
             self.page_faults += 1
             self.handle_page_fault(page_number)
        
        pass # Pula pq por enquanto não tem implementação

    def handle_page_fault(self, page_number):
        """
        Trata uma falha de página.
        Deve encontrar uma moldura livre ou aplicar o FIFO se a memória estiver cheia.
        """
        # TODO: integrante 2 mexe aqui
        
        print(f"[Simulator Stub] Tratando Page Fault para {page_number}. (Lógica de I2 pendente)")
        pass 

    def load_page(self, page_number, frame_number):
        """
        Função auxiliar para carregar uma página em uma moldura.
        Atualiza memória, tabela e fila.
        """
        # TODO: integrante 2 mexe aqui
        
        print(f"[Simulator Stub] Carregando pág {page_number} na moldura {frame_number}. (Lógica de I2 pendente)")
        pass # 

    def translate_address(self, virtual_address):
        """
        Converte um endereço virtual em um número de página.
        
        PROVISÓRIO: Assume que o endereço já é o número da página.
        """
        # TODO: integrante 1 mexe aqui
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
            "page_table": self.page_table,
            "physical_memory": self.physical_memory,
            "page_faults_count": self.page_faults,
            "last_accessed_page": last_page_accessed,
            "page_fault_occurred": False # Integrante 2 deve atualizar isso em access_page
        }

    def get_final_report(self):
        """
        Empacota o relatório final para a interface.
        Esta é uma função de integração (I3).
        """
        return {
            "total_page_faults": self.page_faults,
            "final_page_table": str(self.page_table),
            "final_physical_memory": str(self.physical_memory)
        }