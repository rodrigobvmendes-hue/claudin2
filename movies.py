#!/usr/bin/env python3
"""Movie recommendation matcher - finds films both partners will enjoy."""

from dataclasses import dataclass, field


@dataclass
class Movie:
    title: str
    year: int
    tags: list[str] = field(default_factory=list)
    streaming: list[str] = field(default_factory=list)

    def score_against(self, other_tags: set[str]) -> int:
        return len(set(self.tags) & other_tags)


KNOWN_MOVIES: list[Movie] = [
    # --- User's list ---
    Movie("Interestelar", 2014, ["sci-fi", "mente", "tempo", "épico", "twist", "drama", "nolan"]),
    Movie("V de Vingança", 2006, ["ação", "distopia", "político", "vingança", "thriller"]),
    Movie("Grande Truque", 2006, ["mistério", "mágica", "twist", "thriller", "nolan", "mente"]),
    Movie("Truque de Mestre", 2013, ["mágica", "heist", "thriller", "twist", "ação"]),
    Movie("Os Suspeitos", 1995, ["crime", "mistério", "twist", "thriller", "policial"]),
    # --- Spouse's list ---
    Movie("Os Outros", 2001, ["terror", "sobrenatural", "twist", "psicológico", "suspense"]),
    Movie("Sexto Sentido", 1999, ["sobrenatural", "twist", "psicológico", "drama", "suspense"]),
    Movie("Seven", 1995, ["crime", "dark", "psicológico", "thriller", "policial"]),
    Movie("Por Trás de Seus Olhos", 2021, ["sobrenatural", "twist", "psicológico", "suspense", "obsessão"]),
    Movie("Efeito Borboleta", 2004, ["sci-fi", "tempo", "psicológico", "drama", "twist", "mente"]),
    Movie("Um Contratempo", 2016, ["crime", "mistério", "twist", "thriller", "suspense"]),
]

CATALOG: list[Movie] = [
    Movie("Ilha do Medo", 2010,
          ["psicológico", "twist", "mistério", "thriller", "mente", "suspense"],
          ["Netflix", "Prime Video", "Apple TV+"]),
    Movie("Memento", 2000,
          ["psicológico", "mistério", "twist", "mente", "crime", "nolan"],
          ["Prime Video", "Telecine"]),
    Movie("A Garota no Trem", 2016,
          ["psicológico", "mistério", "suspense", "thriller", "twist"],
          ["Netflix", "Prime Video"]),
    Movie("Garota Exemplar", 2014,
          ["psicológico", "thriller", "mistério", "twist", "dark", "crime"],
          ["Disney+", "Star+"]),
    Movie("Inception", 2010,
          ["sci-fi", "mente", "tempo", "twist", "ação", "épico", "nolan"],
          ["Max", "Prime Video"]),
    Movie("O Jogo", 1997,
          ["psicológico", "thriller", "mistério", "twist", "suspense"],
          ["Prime Video", "Telecine"]),
    Movie("Prisioneiros", 2013,
          ["crime", "dark", "policial", "drama", "thriller", "psicológico"],
          ["Prime Video", "Max"]),
    Movie("Black Swan", 2010,
          ["psicológico", "thriller", "dark", "obsessão", "suspense"],
          ["Disney+", "Star+", "Prime Video"]),
    Movie("A Mente Brilhante", 2001,
          ["psicológico", "drama", "mente", "twist", "épico"],
          ["Prime Video", "Telecine"]),
    Movie("Clube da Luta", 1999,
          ["psicológico", "twist", "dark", "ação", "mente", "thriller"],
          ["Disney+", "Star+"]),
    Movie("Oldboy", 2003,
          ["psicológico", "vingança", "twist", "dark", "thriller", "crime"],
          ["Prime Video"]),
    Movie("Parasite", 2019,
          ["thriller", "dark", "twist", "crime", "drama", "suspense"],
          ["Max", "Apple TV+"]),
    Movie("Knives Out", 2019,
          ["mistério", "crime", "twist", "thriller", "suspense", "policial"],
          ["Netflix"]),
    Movie("A Testemunha", 1957,
          ["mistério", "crime", "twist", "thriller", "policial", "suspense"],
          ["Prime Video", "Mubi"]),
    Movie("Annihilation", 2018,
          ["sci-fi", "psicológico", "thriller", "mente", "sobrenatural"],
          ["Netflix", "Prime Video"]),
    Movie("A Chegada", 2016,
          ["sci-fi", "mente", "tempo", "drama", "épico", "twist"],
          ["Prime Video", "Max"]),
    Movie("1408", 2007,
          ["sobrenatural", "terror", "psicológico", "suspense", "mente"],
          ["Prime Video", "Telecine"]),
    Movie("Coherence", 2013,
          ["sci-fi", "mente", "thriller", "tempo", "twist", "suspense"],
          ["Prime Video", "Mubi"]),
    Movie("Predestination", 2014,
          ["sci-fi", "tempo", "twist", "thriller", "mente"],
          ["Prime Video", "Netflix"]),
    Movie("Gone Girl", 2014,
          ["psicológico", "thriller", "mistério", "twist", "dark", "crime"],
          ["Disney+", "Star+"]),
    Movie("Ex Machina", 2014,
          ["sci-fi", "psicológico", "thriller", "mente", "twist"],
          ["Prime Video", "Netflix"]),
    Movie("O Labirinto do Fauno", 2006,
          ["sobrenatural", "dark", "drama", "fantasia", "psicológico"],
          ["Max", "Prime Video"]),
    Movie("Haunting of Hill House", 2018,
          ["sobrenatural", "terror", "psicológico", "drama", "twist"],
          ["Netflix"]),
    Movie("Dark (série)", 2017,
          ["sci-fi", "tempo", "twist", "psicológico", "mente", "dark"],
          ["Netflix"]),
    Movie("Ozark", 2017,
          ["crime", "thriller", "dark", "drama", "suspense", "policial"],
          ["Netflix"]),
]


def build_tag_profile(movies: list[Movie]) -> dict[str, int]:
    profile: dict[str, int] = {}
    for movie in movies:
        for tag in movie.tags:
            profile[tag] = profile.get(tag, 0) + 1
    return profile


def top_tags(profile: dict[str, int], n: int = 10) -> set[str]:
    return {tag for tag, _ in sorted(profile.items(), key=lambda x: -x[1])[:n]}


def rank_recommendations(
    user_tags: set[str],
    spouse_tags: set[str],
    already_seen: set[str],
) -> list[tuple[Movie, int, int]]:
    results = []
    for movie in CATALOG:
        if movie.title.lower() in already_seen:
            continue
        u = movie.score_against(user_tags)
        s = movie.score_against(spouse_tags)
        combined = u + s
        if u > 0 and s > 0:
            results.append((movie, u, s))
    results.sort(key=lambda x: -(x[1] + x[2]))
    return results


def analyze(user_movies: list[Movie], spouse_movies: list[Movie]) -> None:
    user_profile = build_tag_profile(user_movies)
    spouse_profile = build_tag_profile(spouse_movies)
    user_tags = top_tags(user_profile)
    spouse_tags = top_tags(spouse_profile)
    seen = {m.title.lower() for m in user_movies + spouse_movies}

    print("\n" + "=" * 60)
    print("  CRUZAMENTO DE GOSTOS - RECOMENDADOR DE FILMES")
    print("=" * 60)

    print(f"\n Perfil de quem perguntou → tags dominantes:")
    top_u = sorted(user_profile.items(), key=lambda x: -x[1])[:6]
    print("  " + ", ".join(f"{t}({n})" for t, n in top_u))

    print(f"\n Perfil da esposa → tags dominantes:")
    top_s = sorted(spouse_profile.items(), key=lambda x: -x[1])[:6]
    print("  " + ", ".join(f"{t}({n})" for t, n in top_s))

    shared = set(user_profile) & set(spouse_profile)
    print(f"\n Tags em comum: {', '.join(sorted(shared))}")

    ranked = rank_recommendations(user_tags, spouse_tags, seen)

    print("\n" + "=" * 60)
    print("  TOP RECOMENDAÇÕES PARA OS DOIS")
    print("=" * 60)

    for i, (movie, u_score, s_score) in enumerate(ranked[:8], 1):
        bar_u = "█" * u_score
        bar_s = "█" * s_score
        streaming = ", ".join(movie.streaming) if movie.streaming else "Locação/Compra digital"
        print(f"\n  {i}. {movie.title} ({movie.year})")
        print(f"     Você    : {bar_u or '·'}  ({u_score} pts)")
        print(f"     Esposa  : {bar_s or '·'}  ({s_score} pts)")
        print(f"     Onde ver: {streaming}")
        print(f"     Tags    : {', '.join(movie.tags)}")

    best = ranked[0][0] if ranked else None
    if best:
        streaming = ", ".join(best.streaming) if best.streaming else "Locação/Compra digital"
        print("\n" + "=" * 60)
        print(f"  MATCH PERFEITO → {best.title} ({best.year})")
        print("=" * 60)
        print(f"  Onde ver: {streaming}")
        print(f"  Tags    : {', '.join(best.tags)}\n")


def main() -> None:
    user_movies = [m for m in KNOWN_MOVIES if m.title in {
        "Interestelar", "V de Vingança", "Grande Truque",
        "Truque de Mestre", "Os Suspeitos",
    }]
    spouse_movies = [m for m in KNOWN_MOVIES if m.title in {
        "Os Outros", "Sexto Sentido", "Seven",
        "Por Trás de Seus Olhos", "Efeito Borboleta", "Um Contratempo",
    }]
    analyze(user_movies, spouse_movies)


if __name__ == "__main__":
    main()
