// src/api/tests/apiService.spec.js
import axios from 'axios';

describe('Testes de apiService', () => {
  it('Deve retornar dados da API de usuários', async () => {
    const response = await axios.get('https://jsonplaceholder.typicode.com/users');
    expect(response.status).toBe(200);
    expect(response.data).toBeDefined();
  });
});