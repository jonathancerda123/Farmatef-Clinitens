# 008 — Búsqueda y entrega de recetas simuladas

Fecha: 2026-11-04. Estado: implementación local en curso. Fuente: solicitud de la usuaria para crear el apartado «Recetas». Código autorizado: sí.

## Problema y resultado

FarmaTEF muestra el flujo de recetas como planificado, pero no tiene modelos ni rutas de receta/dispensación. Se implementará una sección para que personal docente/administre recetas ficticias, las busque por número único y registre una entrega simulada con descuento atómico de inventario.

## Alcance y límites

- Solo datos sintéticos; no se procesan recetas reales ni datos identificables de pacientes. El campo de persona es un alias ficticio.
- MANAGER gestiona sus propias recetas y su inventario; ADMIN/superusuario activo ve el ámbito global conforme a permisos actuales.
- Crear receta con número único, alias, vencimiento y una o más líneas de medicamento/unidades.
- Buscar receta por número, ver el detalle y estado, registrar entrega completa.
- Dispensar todas las líneas en una sola transacción, usando lotes vigentes con vencimiento más próximo (FEFO).
- Sin entrega parcial; si receta vencida, ya entregada o stock insuficiente, no se descuenta nada.
- No incluye acceso RESTRICTED/estudiante, cursos/matrículas, prescripción clínica, firma, PDF ni integración externa. La autorización estudiantil requiere un vínculo curso/actividad que hoy FarmaTEF no tiene.

## Requisitos y aceptación

- RF-008-01: Número de receta único; formulario valida al menos una línea y cantidades positivas.
- RF-008-02: La búsqueda filtra por propiedad del gestor/rol global en servidor.
- RF-008-03: Entrega consume solo lotes vigentes y deja cero si el lote se agota; todo el flujo es atómico y auditable por lote.
- RF-008-04: Estado entregado y usuario/hora se registran una sola vez.
- RF-008-05: Estados de receta vencida, ya entregada, sin stock y éxito aparecen claramente.
- RF-008-06: El flujo y cada entrega indican que son simulados.

## Supuestos

Entrega completa, sin sustitución terapéutica ni instrucciones clínicas; una receta no se dispensa después de su fecha de vigencia. El personal docente registra los datos ficticios. Revisar reglas con la docente antes de usar fuera del prototipo.
