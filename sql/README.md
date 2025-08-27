# 📄 SQL Scripts - NOTA IMPORTANTE

## ⚠️ Scripts SQL No Necesarios

**Este proyecto ahora usa SQLite con SQLAlchemy ORM**, por lo que **no necesitas scripts SQL externos**.

### 🎯 ¿Qué cambió?

- ❌ **Antes**: PostgreSQL + Scripts SQL manuales
- ✅ **Ahora**: SQLite + SQLAlchemy ORM automático

### 🔧 ¿Cómo se crean las tablas ahora?

Las tablas se crean automáticamente usando los **modelos Python** definidos en `app.py`:

```python
# Los modelos en app.py definen la estructura:
class EmpresaTuristica(db.Model):
    # ... definición de campos

class SolicitudVisita(db.Model):
    # ... definición de campos

# Y se crean automáticamente con:
db.create_all()
```

### 🚀 Para crear/recrear la base de datos:

```bash
python scripts/setup/configurar_sistema.py
```

**¡Es todo automático!** 🎉
