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
(Sin implementar)
