# ✅ Tester que l'API répond (GET)
curl http://localhost:8508/

# ➕ Addition : 5 + 3
curl -X POST http://localhost:8000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'

# ✖️ Multiplication : 4 × 7
curl -X POST http://localhost:8000/multiply \
  -H "Content-Type: application/json" \
  -d '{"a": 4, "b": 7}'

# ➗ Division : 10 ÷ 2
curl -X POST http://localhost:8000/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 2}'

# ❌ Division par zéro (doit retourner erreur 400)
curl -X POST http://localhost:8000/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 0}'