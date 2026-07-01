from .inclinacao_lateral import InclinacaoLateral
from .elevacao_frontal_unilateral import ElevacaoFrontalUnilateral
from .elevacao_lateral_bilateral import ElevacaoLateralBilateral


def criar_exercicio(
    nome,
    lado,
    dificuldade
):

    if nome == "Inclinação Lateral":
        return InclinacaoLateral(
            lado,
            dificuldade
        )

    if nome == "Elevação Frontal":
        return ElevacaoFrontalUnilateral(
            lado,
            dificuldade
        )

    if nome == "Elevação Lateral":
        return ElevacaoLateralBilateral(
            lado,
            dificuldade
        )

    raise ValueError(
        f"Exercício desconhecido: {nome}"
    )