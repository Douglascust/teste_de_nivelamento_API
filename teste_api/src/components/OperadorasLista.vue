<template>
  <div class="container">
    <input
      type="text"
      v-model="searchTerm"
      placeholder="Buscar operadora..."
      class="search-input"
      :class="{ 'error-input': inputError }"
      @keydown.enter="search"
    />
    <button @click="search" class="search-button">Buscar</button>
    <div v-if="inputError" class="error-message">Por favor, insira um termo de busca.</div>
    <div v-if="searchError" class="error-message">Nenhuma operadora encontrada.</div>
    <div v-if="exibirDados">
      <h2 class="title">Operadoras</h2>
      <div class="pagination">
        <button
          @click="prevPage"
          :disabled="currentPage <= 1"
          class="pagination-button"
          :class="{ disabled: currentPage <= 1 }"
        >
          Anterior
        </button>
        <span class="page-number">Página {{ currentPage }}</span>
        <button
          @click="nextPage"
          class="pagination-button"
          :disabled="isLastPage"
        >
          Próximo
        </button>
      </div>
      <div class="data-display">
        <div v-for="(operadora, index) in responseFromServer" :key="index" class="operadora-item">
          <div v-for="(value, key) in operadora" :key="key">
            <strong>{{ key }}:</strong> {{ value }}
          </div>
          <hr />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      operadoras: [],
      searchTerm: '',
      currentPage: 1,
      responseFromServer: null,
      exibirDados: false,
      inputError: false,
      searchError: false,
      isLastPage: false,
    };
  },
  mounted() {
    // exibir apenas após a pesquisa
  },
  methods: {
    fetchOperadoras() {
      axios.get(`http://127.0.0.1:5000/operadoras?pagina=${this.currentPage}&termo=${this.searchTerm}`)
        .then((response) => {
          console.log('Resposta do Axios:', response);
          this.responseFromServer = response.data;
          if (Array.isArray(response.data) && response.data.length > 0) {
            this.operadoras = response.data;
            this.searchError = false;
            this.exibirDados = true;
            this.isLastPage = response.data.length < 10;
          } else if (response.data && response.data.error) {
            console.error('Erro do servidor:', response.data.error);
            this.operadoras = [];
            alert('Ocorreu um erro ao buscar as operadoras. Por favor, tente novamente mais tarde.');
            this.searchError = false;
            this.exibirDados = false;
            this.isLastPage = true;
          } else if (Array.isArray(response.data) && response.data.length === 0 && this.currentPage === 1) {
            this.operadoras = [];
            this.searchError = true;
            this.exibirDados = false;
            this.isLastPage = true;
          } else {
            this.operadoras = [];
            this.searchError = false;
            this.exibirDados = true;
            this.isLastPage = true;
          }
          console.log('Dados recebidos:', this.operadoras);
        })
        .catch((error) => {
          console.error('Erro na requisição:', error);
          this.operadoras = [];
          alert('Ocorreu um erro ao buscar as operadoras. Por favor, verifique sua conexão com a internet.');
          this.searchError = false;
          this.exibirDados = false;
          this.isLastPage = true;
        });
    },
    search() {
      this.inputError = false;
      this.searchError = false;
      this.exibirDados = false;
      this.isLastPage = false;

      if (!this.searchTerm.trim()) {
        this.inputError = true;
        return;
      }
      this.currentPage = 1;
      this.fetchOperadoras();
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchOperadoras();
      }
    },
    nextPage() {
      this.currentPage++;
      this.fetchOperadoras();
    },
  },
};
</script>

<style scoped>
.container {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.7), rgba(224, 239, 245, 0.7));
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  border-radius: 8px;
  font-family: sans-serif;
  margin-top: -70px;
}

.search-input {
  padding: 10px 15px;
  border: 2px solid rgba(0, 0, 0, 0.4);
  border-radius: 8px;
  margin-bottom: 5px;
  width: 300px;
  font-size: 16px;
  outline: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-right: 1%;
}

.search-button {
  padding: 10px 20px;
  background-color: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 10px;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #333;
}

.title {
  color: #333;
  margin-bottom: 15px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.pagination-button {
  padding: 10px 20px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 8px;
  margin: 0 10px;
  cursor: pointer;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.pagination-button:hover {
  background-color: #d0d0d0;
  color: #333;
}

.pagination-button.disabled {
  background-color: #e0e0e0;
  color: #999;
  cursor: default;
}

.pagination-button.disabled:hover {
  background-color: #e0e0e0;
  color: #999;
}

.page-number {
  font-weight: bold;
  margin: 0 15px;
  font-size: 16px;
}

.data-display {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #eee;
  overflow-x: auto;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: monospace;
  text-align: left;
  margin-top: 20px;
}

.operadora-item {
  margin-bottom: 10px;
}

.error-input {
  border-color: red;
}

.error-message {
  color: red;
  margin-top: 5px;
  text-align: center;
}

.input-error-message {
  color: red;
  margin-top: 5px;
  text-align: center;
}
</style>