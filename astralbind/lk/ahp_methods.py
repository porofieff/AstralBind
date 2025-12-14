import json
import random
import statistics as stat

import numpy as np
from chat.models import Message, Pair_room
from django.urls import reverse

from .forms import CommentForm, CustomUserCreationForm, UserProfileForm
from .models import (
    City,
    Comment,
    Education,
    Favorite,
    Hobby,
    HobbyGroup,
    UserFilters,
    UserProfile,
    ZodiacSign,
)

translate = {"1": 0.2, "2": 0.3, "3": 1.0, "4": 3.0, "5": 5.0}

RI = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
}


def norm_calculate(matrix) -> list:
    weight_criter = []
    arr_avg_geom = []

    for i in matrix:
        elem_matrix = [float(j) for j in i]
        avg_geom = stat.geometric_mean(elem_matrix)
        arr_avg_geom.append(avg_geom)

    for i in range(len(arr_avg_geom)):
        value = arr_avg_geom[i] / sum(arr_avg_geom)
        weight_criter.append(value)

    return weight_criter


def matrix_filling(
    city_vs_hobby,
    city_vs_zodiac,
    city_vs_education,
    education_vs_hobby,
    education_vs_zodiac,
    hobby_vs_zodiac,
) -> np.ndarray:
    matrix = np.ones((4, 4), dtype=float)
    matrix[0][1] = city_vs_hobby
    matrix[1][0] = 1 / city_vs_hobby
    matrix[0][2] = city_vs_zodiac
    matrix[2][0] = 1 / city_vs_zodiac
    matrix[0][3] = city_vs_education
    matrix[3][0] = 1 / city_vs_education
    matrix[1][3] = 1 / education_vs_hobby
    matrix[3][1] = education_vs_hobby
    matrix[2][3] = 1 / education_vs_zodiac
    matrix[3][2] = education_vs_zodiac
    matrix[1][2] = hobby_vs_zodiac
    matrix[2][1] = 1 / hobby_vs_zodiac

    return matrix


def get_weight_critier(matrix) -> list:
    weight = []
    arr_avg_geom = []

    for i in matrix:
        elem_matrix = [float(j) for j in i]
        avg_geom = stat.geometric_mean(elem_matrix)
        arr_avg_geom.append(avg_geom)

    for i in range(len(arr_avg_geom)):
        value = arr_avg_geom[i] / sum(arr_avg_geom)
        weight.append(value)

    return weight


def get_user_CR(matrix) -> int:
    w = matrix.sum(axis=0)
    normalized_matrix = matrix / w
    w = normalized_matrix.mean(axis=1)
    matrixw = matrix.dot(w)
    lambda_max = np.mean(matrixw / w)
    n = matrix.shape[0]

    CI = (lambda_max - n) / (n - 1)

    return CI / RI.get(len(matrix)) * 100
