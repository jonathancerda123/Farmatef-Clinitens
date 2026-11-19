# 029 — Tres fichas clínicas con avances distintos en la demo 8025

Fecha: 2026-11-18. El usuario solicitó rellenar fichas de simulación con datos coherentes. La captura apunta a la ficha 4. La demo tiene una cuenta de estudiante y cinco fichas de esa cuenta. Se usan la ficha 4 y dos borradores de la misma cuenta para representar los tres avances.

| Requisito | Ficha de la demo | Resultado esperado |
|---|---|---|
| RF-029-01 | 4 · `FCE-APS028-01` | 13 de 13 secciones resueltas, con dos recontroles. Dispositivos invasivos queda como No aplica porque no se instaló ninguno. Mantener el envío pendiente de calificación. |
| RF-029-02 | 5 · `FCE-APS028-02` | Borrador con seis de 13 secciones completas y siete pendientes. |
| RF-029-03 | 3 · `FCE-INT-03` | Borrador con tres de 13 secciones completas y diez pendientes. Sustituir la fila de prueba de tratamiento por un antecedente ficticio congruente. |

La progresión se mide con `seccion_completa` y se verifica en Seguimiento en vivo. Se preservan los pacientes SIM, el curso, la cuenta, las evaluaciones y las demás fichas. Los contenidos son ficticios y respetan los signos o antecedentes ya presentes en los casos.
