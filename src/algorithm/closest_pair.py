from config import *  

# a distância é a hipotenusa do nosso triangulo retangulo formado por (x2 - x1), (y2 - y1) e a hipotenusa
def get_distance(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2) ** 0.5

def divide_conquer(px: list, py: list) -> tuple:
    # condição de parada é não ter mais de 1 ponto
    if len(px) <= 1:
        return (INF, None, None)

    mid = (len(px) // 2)
    # divide px em duas metades pela posição mediana
    left_px = px[:mid]
    right_px = px[mid:]

    # é o ponto em que a linha divisória passa
    line_x = px[mid - 1].x

    # mantém a ordenação por y filtrando quais pontos pertencem à metade esquerda e direita
    # como a gnt usa <= line_x, o ponto mediano é contabilizado para os pontos à esquerda
    left_py = [p for p in py if p.x <= line_x]
    right_py = [p for p in py if p.x > line_x]

    # resolve recursivamente cada metade
    (distance_left, a_left, b_left) = divide_conquer(left_px, left_py)
    (distance_right, a_right, b_right) = divide_conquer(right_px, right_py)

    # seleciona o menor resultado entre as duas metades
    if distance_left < distance_right:
        d_min = distance_left
        p1_min = a_left
        p2_min = b_left
    else:
        d_min = distance_right
        p1_min = a_right
        p2_min = b_right

    # pegando os pontos que estão a uma distancia d_min (no eixo x) do ponto que é a linha divisória
    points_range = [p for p in py if abs(p.x - line_x) < d_min]

    # verificando a distancia entre esses pontos para achar o par mais próximo 
    for i in range(len(points_range)):
        # por prova geométrica, só é necessário comparar cada ponto com até os x próximos no strip
        for j in range(i + 1, min(i + 7, len(points_range))):
            p1 = points_range[i]
            p2 = points_range[j]
            dist = get_distance(p1, p2)
            if dist < d_min:
                d_min = dist
                p1_min = p1
                p2_min = p2

    return (d_min, p1_min, p2_min)

def closest_pair(asteroids):
    # se houver menos de dois pontos, não existe par válido
    if len(asteroids) < 2:
        return (INF, None, None)

    # cria listas ordenadas por x e por y para a etapa de divisão e conquista 
    px = sorted(asteroids, key=lambda asteroid: asteroid.x)
    py = sorted(asteroids, key=lambda asteroid: asteroid.y)

    return divide_conquer(px, py)
