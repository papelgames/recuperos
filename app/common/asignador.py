from app.auth.models import User
from app.models import Recuperos

def asignar():
    usuarios_activos = User.get_by_perfil_activo('Analista')
    ultimo_usuario_grabado = Recuperos.get_ultimo_registro().usuario_responsable
    usuarios_lista = []
    for usuarios in usuarios_activos:
        usuarios_lista.append(usuarios.id)
    
    print(len(usuarios_lista)-1)
    print(usuarios_lista.index(ultimo_usuario_grabado))
    if ultimo_usuario_grabado in usuarios_lista:
        if len(usuarios_lista)-1 == usuarios_lista.index(ultimo_usuario_grabado):
            
            print("uno")
            return usuarios_lista[0]
        else:
            print("dos")
            return usuarios_lista[usuarios_lista.index(ultimo_usuario_grabado)+1]
    else:
        print("tres")
        return usuarios_lista[0] 
