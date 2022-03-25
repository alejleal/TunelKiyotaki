# TunelKiyotaki
Práctica 2: Túnel de Kiyotaki

Simula el funcionamiento de un túnel que permite el paso de coches en una sola dirección.

# 01_sol_skel
Se configura el monitor con dos semáforos. Con la condición de que los coches con una dirección pasará cuando no haya coches circulando en la otra dirección.
-Problemas:
    1.-Justicia: No se controla el orden de paso de los coches. Por tanto podría pasar que los coches de una dirección se queden esperando hasta que hayan pasado todos los de la otra dirección.
    2.-Los coches de una misma dirección no tienen establecido ningún orden. Un coche esperando en una dirección puede entrar después de otro coche posterior a él en la misma dirección.

# 02_sol_skel
Funciona de manera similar a la versión anterior. Se controlan el paso de los coches comprobando la dirección de circulación del tunel, de manera que permite el paso si coinciden con la propia dirección. Y se cambia esta cuando no haya coches y pase un coche que actualize esta dirección.

# 03_sol_skel
(Implementado)(Falta comprobar)

# 04_sol_skel
(Falta por implementar)

# 05_sol_skel
Se intenta solucionar el problema de la justicia reforzando la condition. Se introduce dos semáforos más que controlan la entra de coches permitiendo el paso si no hay coche circulando en la otra dirección(análogo a 01_sol_skel) y además si hay menos de un número determinado de coches esperando el el otro sentido.

Esto lo controla la variables: "north_cars_waiting" y "south_cars_waiting" y los condicionales "too_many_north_cars" y "too_many_south_cars".

Las variables K1 y K2 es la cota de coches esperando. Estaría bien hacer que esta variable no fuese constante. Haciendo que por cada coche que pase en una dirección, la variable disminuya de valor hasta 0, permitiendo que los coches en la otra dirección sean más posibles para pasar, ya que restringe los coches de su propia dirección.
Después se debería reestablecer su valor cuando los coches de la otra dirección empiecen a pasar.

Se ha hecho pruebas para ver que sigue funcionando igual que la versión 1. Pero no se comprobado que solucione el problema. Teóricamente parece que sí lo soluciona. <3