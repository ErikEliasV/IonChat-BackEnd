## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Cadastro de Usuário

**Endpoint:** `POST /api/users/register/`

**Descrição:** Cria um novo usuário no sistema.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "first_name": "João",
    "last_name": "Silva",
    "email": "joao@email.com",
    "password": "minhasenha123",
    "password_confirm": "minhasenha123"
}
```

**Resposta de Sucesso (201):**
```json
{
    "message": "Usuário cadastrado com sucesso!",
    "user": {
        "id": "9c8a57a6-c9d2-4415-9c79-93448957b5bd",
        "first_name": "João",
        "last_name": "Silva",
        "email": "joao@email.com"
    }
}
```

**Resposta de Erro (400):**
```json
{
    "message": "Erro ao cadastrar usuário",
    "errors": {
        "email": ["Este email já está em uso."],
        "password_confirm": ["As senhas não coincidem."]
    }
}
```

**Validações:**
- Email deve ser único
- Senhas devem coincidir
- Todos os campos são obrigatórios
- Senha deve atender aos critérios de segurança do Django

---

### 2. Buscar Usuário por ID

**Endpoint:** `GET /api/users/{id}/`

**Descrição:** Retorna os dados de um usuário específico pelo ID.

**Parâmetros:**
- `id` (UUID): ID único do usuário

**Resposta de Sucesso (200):**
```json
{
    "user": {
        "id": "9c8a57a6-c9d2-4415-9c79-93448957b5bd",
        "first_name": "João",
        "last_name": "Silva",
        "full_name": "João Silva",
        "email": "joao@email.com",
        "created_at": "2025-10-01T21:57:00.123456Z",
        "is_online": false
    }
}
```

**Resposta de Erro (404):**
```json
{
    "detail": "Not found."
}
```

---

### 3. Login de Usuário

**Endpoint:** `POST /api/users/login/`

**Descrição:** Autentica um usuário e retorna tokens JWT.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "email": "joao@email.com",
    "password": "minhasenha123"
}
```

**Resposta de Sucesso (200):**
```json
{
    "message": "Login realizado com sucesso!",
    "user": {
        "id": "9c8a57a6-c9d2-4415-9c79-93448957b5bd",
        "first_name": "João",
        "last_name": "Silva",
        "full_name": "João Silva",
        "email": "joao@email.com",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

**Resposta de Erro (400):**
```json
{
    "message": "Erro ao fazer login",
    "errors": {
        "non_field_errors": ["Credenciais inválidas."]
    }
}
```

**Validações:**
- Email e senha são obrigatórios
- Credenciais devem ser válidas
- Usuário deve estar ativo
- Access token válido por 3 dias
- Refresh token válido por 7 dias

---

## Exemplo de Uso

### cURL

**Cadastro de Usuário:**
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "João",
    "last_name": "Silva",
    "email": "joao@email.com",
    "password": "minhasenha123",
    "password_confirm": "minhasenha123"
  }'
```

**Buscar Usuário por ID:**
```bash
curl -X GET http://localhost:8000/api/users/9c8a57a6-c9d2-4415-9c79-93448957b5bd/
```

**Login de Usuário:**
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com",
    "password": "minhasenha123"
  }'
```
