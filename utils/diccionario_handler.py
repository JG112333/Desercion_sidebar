# Diccionarios de mapeo para convertir texto a números
estado_civil_map = {
    "Soltero": 1,
    "Casado": 2,
    "Viudo": 3,
    "Divorciado": 4,
    "Union de Facto": 5,
    "Separado Legalmente": 6
}

modo_admision_map = {
    "Admisión general 1ra fase: Admisión en la fase estándar del proceso de selección.": 1,
    "Admisión por normativa especial: Estudiante con modalidad de acceso bajo reglamentación especial.": 2,
    "Admisión por contingente especial: Admisión bajo condiciones especiales para grupos específicos de estudiantes.": 3,
    "Titulares de otros títulos universitarios: Personas con estudios previos en educación superior.": 4,
    "Estudiante con modalidad de acceso por normativa especial para personas con formación no convencional.": 5,
    "Estudiante internacional (licenciatura): Estudiante extranjero que aplica para un programa de licenciatura.": 6,
    "Admisión por contingente especial (otros grupos): Admisión bajo condiciones especiales para otros grupos fuera de la norma general.": 7,
    "Admisión general 2da fase: Admisión en fase posterior al proceso estándar de selección.": 8,
    "Admisión general 3ra fase: Admisión en fase posterior al proceso estándar y 2da fase de selección.": 9,
    "Admisión bajo plan alternativo: Admisión bajo un plan o acuerdo alternativo específico.": 10,
    "Admisión por estudios previos en otra institución.": 11,
    "Mayor de 23 años: Estudiantes mayores de 23 años que aplican para estudios superiores.": 12,
    "Transferencia de institución.": 13,
    "Cambio de carrera o programa: Estudiante que desea cambiar su área de estudio en la universidad.": 14,
    "Admisión por segunda carrera.": 15,
    "Cambio de institución o carrera.": 16,
    "Admisión por título de ciclo corto.": 17,
    "Cambio de institución/carrera (internacional).": 18
}

asistencia_map = {
    "Vespertino": 0,
    "Diurno": 1
}

cualificacion_previa_map = {
    "Educación secundaria": 1,
    "Educación superior—título de licenciatura": 2,
    "Educación superior—título universitario": 3,
    "Educación superior—título de maestría": 4,
    "Educación superior—doctorado": 5,
    "Frecuencia de educación superior": 6,
    "12° año de escolaridad—no completado": 7,
    "11° año de escolaridad—no completado": 8,
    "Otro—11° año de escolaridad": 9,
    "10° año de escolaridad": 10,
    "10° año de escolaridad—no completado": 11,
    "Educación básica 3er ciclo (9°/10°/11° año) o equivalente": 12,
    "Educación básica 2° ciclo (6°/7°/8° año) o equivalente": 13,
    "Curso de especialización tecnológica": 14,
    "Educación superior—título universitario (1er ciclo)": 15,
    "Curso técnico profesional superior": 16,
    "Educación superior—título de maestría (2° ciclo)": 17
}

ocupacion_madre_map = {
    "Estudiante": 1,
    "Representantes del Poder Legislativo y Cuerpos Ejecutivos, Directores, Gerentes y Ejecutivos": 2,
    "Especialistas en Actividades Intelectuales y Científicas": 3,
    "Técnicos de Nivel Intermedio y Profesiones": 4,
    "Personal Administrativo": 5,
    "Trabajadores de Servicios Personales, Seguridad y Protección, y Vendedores": 6,
    "Agricultores y Trabajadores Calificados en Agricultura, Pesca y Silvicultura": 7,
    "Trabajadores Calificados en la Industria, Construcción y Artesanos": 8,
    "Operadores de Instalación y Máquinas y Trabajadores de Ensamblaje": 9,
    "Trabajadores No Calificados": 10,
    "Profesiones de las Fuerzas Armadas": 11,
    "Otra Profesion":12,
    "(vacío)":13,
    "Oficiales de las Fuerzas Armadas":14,
    "Sargentos de las Fuerzas Armadas": 15,
    "Otro Personal de las Fuerzas Armadas":16,
    "Directores de Servicios Administrativos y Comerciales":17,
    "Directores de Hoteles, Restauración, Comercio y Otros Servicios":18,
    "Especialistas en Ciencias Físicas, Matemáticas, Ingeniería y Técnicas Relacionadas":19,
    "Profesionales de la Salud":20,
    "Docentes":21,
    "Especialistas en Finanzas, Contabilidad, Organización Administrativa, y Relaciones Públicas y Comerciales":22,
    "Técnicos de Nivel Intermedio en Ciencias e Ingeniería y Profesiones":23,
    "Técnicos y Profesionales de Nivel Intermedio en Salud":24,
    "Técnicos de Nivel Intermedio en Servicios Legales, Sociales, Deportivos, Culturales y Similares":25,
    "Técnicos en Tecnologías de la Información y la Comunicación":26,
    "Trabajadores de Oficina, Secretarios en General y Operadores de Procesamiento de Datos":27,
    "Operadores de Datos, Contabilidad, Servicios Estadísticos, Financieros y Relacionados con Registros":28,
    "Otro Personal de Apoyo Administrativo":29,
    "Trabajadores de Servicios Personales":30,
    "Vendedores":31,
    "Trabajadores de Cuidado Personal y Similares":32,
    "Personal de Servicios de Protección y Seguridad":33,
    "Agricultores Orientados al Mercado y Trabajadores Calificados en Producción Agrícola y Animal":34,
    "Agricultores, Ganaderos, Pescadores, Cazadores, Recolectores y Subsistencia":35,
    "Trabajadores Calificados en Construcción, Excepto Electricistas":36,
    "Trabajadores Calificados en Metalurgia, Siderurgia y Similares":37,
    "Trabajadores Calificados en Electricidad y Electrónica":38,
    "Trabajadores en Procesamiento de Alimentos, Trabajo en Madera, y la Industria Textil y Otras Artesanías":39,
    "Operadores de Planta Fija y Máquinas":40,
    "Trabajadores de Ensamblaje":41,
    "Conductores de Vehículos y Operadores de Equipos Móviles":42,
    "Trabajadores No Calificados en Agricultura, Producción Animal y Pesca y Silvicultura":43,
    "Trabajadores No Calificados en la Industria Extractiva, Construcción, Manufactura y Transporte":44,
    "Asistentes en Preparación de Comidas":45,
    "Vendedores Ambulantes (Excepto Alimentos) y Proveedores de Servicios en la Calle":46
}

ocupacion_padre_map = ocupacion_madre_map 

desplazado = {
    "No": 0,
    "Sí": 1
}

deudor = {
    "No": 0,
    "Sí": 1
}


matricula_al_dia = {
    "No": 0,
    "Sí": 1
}


genero = {
    "Femenino": 0,
    "Masculino": 1
}


becado = {
    "No": 0,
    "Sí": 1
}

# Crear versiones invertidas de los diccionarios nnnnnnnnnnnnnnnnnnnnn
# estado_civil_inv = {v: k for k, v in estado_civil_map.items()}
# modo_admision_inv = {v: k for k, v in modo_admision_map.items()}
# asistencia_inv = {v: k for k, v in asistencia_map.items()}
# cualificacion_previa_inv = {v: k for k, v in cualificacion_previa_map.items()}
# ocupacion_madre_inv = {v: k for k, v in ocupacion_madre_map.items()}
# ocupacion_padre_inv = {v: k for k, v in ocupacion_padre_map.items()}
# desplazado_inv = {v: k for k, v in desplazado.items()}
# deudor_inv = {v: k for k, v in deudor.items()}
# matricula_al_dia_inv = {v: k for k, v in matricula_al_dia.items()}
# genero_inv = {v: k for k, v in genero.items()}
# becado_inv = {v: k for k, v in becado.items()}
# Verificar que los valores de los diccionarios son cadenas de texto
estado_civil_inv = {v: str(k) for k, v in estado_civil_map.items()}
modo_admision_inv = {v: str(k) for k, v in modo_admision_map.items()}
asistencia_inv = {v: str(k) for k, v in asistencia_map.items()}
cualificacion_previa_inv = {v: str(k) for k, v in cualificacion_previa_map.items()}
ocupacion_madre_inv = {v: str(k) for k, v in ocupacion_madre_map.items()}
ocupacion_padre_inv = {v: str(k) for k, v in ocupacion_padre_map.items()}
desplazado_inv = {v: str(k) for k, v in desplazado.items()}
deudor_inv = {v: str(k) for k, v in deudor.items()}
matricula_al_dia_inv = {v: str(k) for k, v in matricula_al_dia.items()}
genero_inv = {v: str(k) for k, v in genero.items()}
becado_inv = {v: str(k) for k, v in becado.items()}
