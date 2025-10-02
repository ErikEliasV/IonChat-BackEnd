## Base URL
```
http://localhost:8000
```

## Resumo dos Endpoints

| Método | Endpoint | Autenticação | Descrição |
|--------|----------|--------------|-----------|
| POST | `/api/users/register/` | ❌ | Cadastro de usuário |
| POST | `/api/users/login/` | ❌ | Login (retorna JWT) |
| POST | `/api/users/logout/` | ✅ | Logout (marca como offline) |
| POST | `/api/users/ping/` | ✅ | Ping/heartbeat (mantém online) |
| GET | `/api/users/me/` | ✅ | Informações do usuário logado |
| GET | `/api/users/` | ✅ | Lista todos os usuários |
| GET | `/api/users/{id}/` | ❌ | Buscar usuário por ID |

### 🔄 **Como Funciona:**

1. **Login**: Usuário fica online automaticamente
2. **Uso da API**: A cada requisição, `last_seen` é atualizado
3. **App em background**: Usuário continua online
4. **Timeout automático**: Após 5 minutos sem atividade, fica offline automaticamente
5. **Logout manual**: Fica offline imediatamente

### 📱 **Comportamento do App:**

- **App ativo**: Usuário fica online
- **App em background**: Continua online por até 5 minutos
- **App fechado**: Fica offline após 5 minutos
- **Ping/Heartbeat**: App pode enviar ping a cada 30 segundos para manter online

### ⚙️ **Configuração Automática:**

- **Middleware**: Atualiza `last_seen` automaticamente a cada requisição
- **Timeout**: 5 minutos de inatividade = offline automático
- **Ping**: Endpoint `/ping/` para manter usuário online

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
- Access token válido por 24 horas
- Refresh token válido por 7 dias
- **Novo:** Usuário é automaticamente marcado como online após login

---

### 4. Logout de Usuário

**Endpoint:** `POST /api/users/logout/`

**Descrição:** Desautentica o usuário e marca como offline.

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

**Resposta de Sucesso (200):**
```json
{
    "message": "Logout realizado com sucesso!"
}
```

**Resposta de Erro (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

### 5. Ping/Heartbeat

**Endpoint:** `POST /api/users/ping/`

**Descrição:** Mantém o usuário online. Deve ser chamado periodicamente pelo app (ex: a cada 30 segundos) para manter o status online.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de Sucesso (200):**
```json
{
    "message": "Ping recebido",
    "status": "online",
    "last_seen": "2025-10-01T22:30:00.123456Z"
}
```

**Resposta de Erro (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Uso Recomendado:**
- Chamar a cada 30 segundos quando app está ativo
- Chamar a cada 2 minutos quando app está em background
- Não é necessário quando app está fechado

---

### 6. Informações do Usuário Logado

**Endpoint:** `GET /api/users/me/`

**Descrição:** Retorna informações detalhadas do usuário autenticado, incluindo status online/offline e tempo offline.

**Headers:**
```
Authorization: Bearer <access_token>
```

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
        "is_online": true,
        "last_seen": "2025-10-01T22:30:00.123456Z",
        "last_login_time": "2025-10-01T22:30:00.123456Z",
        "time_offline": "Online"
    }
}
```

**Resposta de Erro (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

### 7. Listar Todos os Usuários

**Endpoint:** `GET /api/users/`

**Descrição:** Retorna lista de todos os usuários cadastrados com informações de status online/offline.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de Sucesso (200):**
```json
{
    "users": [
        {
            "id": "9c8a57a6-c9d2-4415-9c79-93448957b5bd",
            "first_name": "João",
            "last_name": "Silva",
            "full_name": "João Silva",
            "email": "joao@email.com",
            "created_at": "2025-10-01T21:57:00.123456Z",
            "is_online": true,
            "last_seen": "2025-10-01T22:30:00.123456Z",
            "time_offline": "Online"
        },
        {
            "id": "8b7a46a5-b8c1-3304-8b68-82337846a4ac",
            "first_name": "Maria",
            "last_name": "Santos",
            "full_name": "Maria Santos",
            "email": "maria@email.com",
            "created_at": "2025-10-01T20:30:00.123456Z",
            "is_online": false,
            "last_seen": "2025-10-01T22:00:00.123456Z",
            "time_offline": "30 minutos"
        }
    ],
    "total": 2
}
```

**Resposta de Erro (401):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Sistema de Status Online/Offline

### Funcionalidades Implementadas

**Controle de Status:**
- Usuários são automaticamente marcados como **online** ao fazer login
- Usuários são marcados como **offline** ao fazer logout
- Sistema rastreia automaticamente o tempo offline

**Campos de Tempo:**
- `is_online`: Boolean indicando status atual
- `last_seen`: Timestamp da última atividade
- `last_login_time`: Timestamp do último login
- `time_offline`: String formatada com tempo offline

**Exemplos de `time_offline`:**
- `"Online"` - quando o usuário está online
- `"30 segundos"` - quando offline há menos de 1 minuto
- `"5 minutos"` - quando offline há menos de 1 hora
- `"2 horas"` - quando offline há menos de 1 dia
- `"3 dias"` - quando offline há mais de 1 dia

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

**Login de Usuário:**
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com",
    "password": "minhasenha123"
  }'
```

**Informações do Usuário Logado (requer token):**
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <seu_access_token>"
```

**Listar Todos os Usuários (requer token):**
```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <seu_access_token>"
```

**Ping/Heartbeat (requer token):**
```bash
curl -X POST http://localhost:8000/api/users/ping/ \
  -H "Authorization: Bearer <seu_access_token>"
```

**Logout (requer token):**
```bash
curl -X POST http://localhost:8000/api/users/logout/ \
  -H "Authorization: Bearer <seu_access_token>"
```

**Buscar Usuário por ID:**
```bash
curl -X GET http://localhost:8000/api/users/9c8a57a6-c9d2-4415-9c79-93448957b5bd/
```
