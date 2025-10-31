from dataclasses import dataclass




@dataclass(frozen=True)
class Cliente:


    nombre: str
    email: str | None = None


    def __post_init__(self): # type: ignore[override]
        if not self.nombre or not self.nombre.strip():
         raise ValueError("El nombre del cliente no puede estar vacío.")
        if self.email is not None and ("@" not in self.email or "." not in self.email):
         raise ValueError("El email del cliente no es válido.")