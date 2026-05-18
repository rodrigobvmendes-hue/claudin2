#!/usr/bin/env python3
"""Movie recommendation matcher - finds films both partners will enjoy."""

from dataclasses import dataclass, field


@dataclass
class Movie:
    title: str
    year: int
    tags: list[str] = field(default_factory=list)
    streaming: list[str] = field(default_factory=list)
    series: bool = False

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

SEEN: set[str] = {
    "gone girl",  # = garota exemplar
    "o ilusionista",
    "ilha do medo",
    "clube da luta",
    "amnésia",
    "memento",
    "o brilho eterno de uma mente sem lembranças",
    "eternal sunshine of the spotless mind",
    "operário",
    "12 macacos",
    "menino do pijama listrado",
    "beleza oculta",
    "garota exemplar",
    "gone girl",
    "inception",
    "parasite",
}

CATALOG: list[Movie] = [
    # ---- Filmes (pré-2020) ----
    Movie("A Garota no Trem", 2016,
          ["psicológico", "mistério", "suspense", "thriller", "twist"],
          ["Netflix", "Prime Video"]),
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
    Movie("Oldboy", 2003,
          ["psicológico", "vingança", "twist", "dark", "thriller", "crime"],
          ["Prime Video"]),
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
    Movie("Ex Machina", 2014,
          ["sci-fi", "psicológico", "thriller", "mente", "twist"],
          ["Prime Video", "Netflix"]),
    Movie("O Labirinto do Fauno", 2006,
          ["sobrenatural", "dark", "drama", "fantasia", "psicológico"],
          ["Max", "Prime Video"]),
    Movie("Premonição", 2007,
          ["sobrenatural", "thriller", "suspense", "twist", "psicológico"],
          ["Prime Video", "Max"]),
    Movie("O Passageiro", 2018,
          ["thriller", "suspense", "ação", "crime", "twist"],
          ["Netflix", "Prime Video"]),
    Movie("O Suspeito", 2013,
          ["crime", "thriller", "mistério", "twist", "policial", "suspense"],
          ["Prime Video"]),
    Movie("Identidade", 2003,
          ["psicológico", "mistério", "twist", "thriller", "crime", "suspense"],
          ["Netflix", "Prime Video"]),
    Movie("Wind River", 2017,
          ["crime", "thriller", "dark", "policial", "suspense", "drama"],
          ["Prime Video", "Star+"]),
    Movie("Segredo nos Olhos", 2009,
          ["crime", "mistério", "thriller", "twist", "suspense", "policial"],
          ["Prime Video"]),
    Movie("O Homem Duplicado", 2013,
          ["psicológico", "mistério", "thriller", "mente", "dark", "twist"],
          ["Prime Video", "Mubi"]),
    Movie("Viveiro", 2019,
          ["sci-fi", "psicológico", "thriller", "dark", "sobrenatural", "mente"],
          ["Prime Video"]),
    Movie("Searching", 2018,
          ["thriller", "mistério", "suspense", "crime", "twist"],
          ["Netflix", "Prime Video"]),
    Movie("Midsommar", 2019,
          ["terror", "psicológico", "dark", "suspense", "sobrenatural"],
          ["Prime Video", "Max"]),
    Movie("Hereditary", 2018,
          ["terror", "sobrenatural", "psicológico", "dark", "drama", "twist"],
          ["Prime Video", "Max"]),
    # ---- Filmes (2020+) ----
    Movie("Tenet", 2020,
          ["sci-fi", "mente", "tempo", "ação", "thriller", "nolan", "twist"],
          ["Max", "Prime Video"]),
    Movie("Last Night in Soho", 2021,
          ["psicológico", "tempo", "thriller", "sobrenatural", "suspense", "twist"],
          ["Prime Video", "Apple TV+"]),
    Movie("Barbarian", 2022,
          ["terror", "psicológico", "dark", "thriller", "twist", "suspense"],
          ["Disney+", "Star+"]),
    Movie("Nope", 2022,
          ["sci-fi", "thriller", "sobrenatural", "suspense", "dark", "twist"],
          ["Prime Video", "Apple TV+"]),
    Movie("The Black Phone", 2022,
          ["terror", "sobrenatural", "thriller", "suspense", "dark", "psicológico"],
          ["Prime Video", "Peacock"]),
    Movie("Men", 2022,
          ["psicológico", "terror", "sobrenatural", "dark", "suspense", "drama"],
          ["Prime Video"]),
    Movie("Glass Onion", 2022,
          ["mistério", "crime", "twist", "thriller", "suspense", "policial"],
          ["Netflix"]),
    Movie("The Menu", 2022,
          ["thriller", "dark", "suspense", "twist", "crime", "psicológico"],
          ["Disney+", "Star+", "Max"]),
    Movie("No Exit", 2022,
          ["thriller", "suspense", "crime", "twist", "ação"],
          ["Disney+", "Star+"]),
    Movie("Crimes do Futuro", 2022,
          ["sci-fi", "psicológico", "dark", "thriller", "mente"],
          ["Prime Video", "Mubi"]),
    Movie("Run Rabbit Run", 2023,
          ["terror", "psicológico", "sobrenatural", "drama", "suspense"],
          ["Netflix"]),
    Movie("Reptile", 2023,
          ["crime", "thriller", "mistério", "policial", "dark", "twist"],
          ["Netflix"]),
    Movie("Saltburn", 2023,
          ["psicológico", "thriller", "dark", "twist", "obsessão", "crime"],
          ["Prime Video"]),
    Movie("Fair Play", 2023,
          ["psicológico", "thriller", "dark", "drama", "obsessão", "suspense"],
          ["Netflix"]),
    Movie("Knock at the Cabin", 2023,
          ["thriller", "sobrenatural", "suspense", "psicológico", "twist", "drama"],
          ["Prime Video", "Peacock"]),
    Movie("Missing", 2023,
          ["thriller", "mistério", "suspense", "crime", "twist"],
          ["Netflix", "Prime Video"]),
    Movie("Talk to Me", 2023,
          ["terror", "sobrenatural", "psicológico", "dark", "suspense", "drama"],
          ["Max", "Prime Video"]),
    Movie("Infinity Pool", 2023,
          ["sci-fi", "psicológico", "dark", "thriller", "sobrenatural", "twist"],
          ["Max", "Prime Video"]),
    Movie("A Haunting in Venice", 2023,
          ["mistério", "sobrenatural", "thriller", "suspense", "policial", "twist"],
          ["Disney+", "Star+"]),
    Movie("The Killer", 2023,
          ["thriller", "crime", "dark", "ação", "suspense", "psicológico"],
          ["Netflix"]),
    Movie("May December", 2023,
          ["psicológico", "drama", "dark", "suspense", "obsessão"],
          ["Netflix", "Max"]),
    Movie("Speak No Evil", 2024,
          ["psicológico", "thriller", "dark", "suspense", "drama", "twist"],
          ["Prime Video"]),
    Movie("The Substance", 2024,
          ["psicológico", "terror", "dark", "thriller", "twist"],
          ["Mubi", "Prime Video"]),
    Movie("Longlegs", 2024,
          ["crime", "dark", "sobrenatural", "policial", "thriller", "suspense"],
          ["Prime Video"]),
    Movie("Trap", 2024,
          ["thriller", "crime", "suspense", "twist", "psicológico"],
          ["Prime Video", "Apple TV+"]),
    Movie("I Saw the TV Glow", 2024,
          ["psicológico", "sobrenatural", "dark", "mente", "drama", "suspense"],
          ["Max", "Prime Video"]),
    Movie("Heretic", 2024,
          ["psicológico", "thriller", "dark", "suspense", "drama", "twist"],
          ["Prime Video"]),
    Movie("MaXXXine", 2024,
          ["terror", "thriller", "dark", "suspense", "crime", "psicológico"],
          ["Max", "Prime Video"]),
    Movie("Oddity", 2024,
          ["terror", "sobrenatural", "thriller", "suspense", "twist", "psicológico"],
          ["Shudder", "Prime Video"]),
    # ---- Séries (marcadas, não aparecem no modo filmes) ----
    Movie("Dark", 2017,
          ["sci-fi", "tempo", "twist", "psicológico", "mente", "dark"],
          ["Netflix"], series=True),
    Movie("Ozark", 2017,
          ["crime", "thriller", "dark", "drama", "suspense", "policial"],
          ["Netflix"], series=True),
    Movie("Haunting of Hill House", 2018,
          ["sobrenatural", "terror", "psicológico", "drama", "twist"],
          ["Netflix"], series=True),
    Movie("The Fall of the House of Usher", 2023,
          ["sobrenatural", "dark", "psicológico", "drama", "thriller", "twist"],
          ["Netflix"], series=True),
    Movie("Baby Reindeer", 2024,
          ["psicológico", "drama", "thriller", "dark", "obsessão", "suspense"],
          ["Netflix"], series=True),
    Movie("Ripley", 2024,
          ["crime", "thriller", "psicológico", "mistério", "dark", "twist"],
          ["Netflix"], series=True),
    Movie("Silo", 2023,
          ["sci-fi", "distopia", "thriller", "mistério", "suspense", "drama"],
          ["Apple TV+"], series=True),
    Movie("Constellation", 2024,
          ["sci-fi", "psicológico", "sobrenatural", "thriller", "tempo", "mente", "twist"],
          ["Apple TV+"], series=True),
    Movie("Black Mirror", 2011,
          ["sci-fi", "psicológico", "dark", "thriller", "mente", "twist", "distopia"],
          ["Netflix"], series=True),
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
    min_year: int = 0,
) -> list[tuple[Movie, int, int]]:
    results = []
    seen_titles: set[str] = set()
    for movie in CATALOG:
        key = movie.title.lower()
        if key in already_seen or key in seen_titles or movie.year < min_year or movie.series:
            continue
        seen_titles.add(key)
        u = movie.score_against(user_tags)
        s = movie.score_against(spouse_tags)
        if u > 0 and s > 0:
            results.append((movie, u, s))
    results.sort(key=lambda x: -(x[1] + x[2]))
    return results


def best_match(ranked: list[tuple[Movie, int, int]]) -> Movie | None:
    # Balanced score = geometric mean favors films where both partners score well
    if not ranked:
        return None
    return max(ranked, key=lambda x: (x[1] * x[2]) * 10 + (x[1] + x[2]))[0]


def analyze(
    user_movies: list[Movie],
    spouse_movies: list[Movie],
    extra_seen: set[str] | None = None,
) -> None:
    user_profile = build_tag_profile(user_movies)
    spouse_profile = build_tag_profile(spouse_movies)
    user_tags = top_tags(user_profile)
    spouse_tags = top_tags(spouse_profile)
    seen = {m.title.lower() for m in user_movies + spouse_movies}
    if extra_seen:
        seen |= {s.lower() for s in extra_seen}

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

    ranked = rank_recommendations(user_tags, spouse_tags, seen, min_year=2020)

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

    best = best_match(ranked)
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
    analyze(user_movies, spouse_movies, extra_seen=SEEN)


if __name__ == "__main__":
    main()
