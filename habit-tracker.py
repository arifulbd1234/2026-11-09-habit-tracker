# Day 34 - 2026-11-09
# Habit Tracker - rojkar valo ovvash gulo track korar chhoto tool.
# Protidin kon habit ta korle, koto din tana (streak) cholche,
# ar kon habit ta miss hocche - eshob ek nazore dekha jay.
# Jara notun ovvash gore tulte chay (namaz, boi pora, exercise,
# pani khawa) tader jonno khub kaje lage.

from datetime import date, timedelta


class HabitTracker:
    """Ekta sohoj habit tracker: habit add kora, check-in kora, streak dekha."""

    def __init__(self):
        # habit name -> set of dates (YYYY-MM-DD) jokhon habit ta kora hoyeche
        self.habits = {}

    def add_habit(self, name):
        """Notun ekta habit jog koro."""
        name = name.strip()
        if not name:
            return "Habit er nam khali rakha jabe na."
        if name in self.habits:
            return f"'{name}' habit ta age thekei ache."
        self.habits[name] = set()
        return f"'{name}' habit ta jog hoye geche."

    def check_in(self, name, on_date=None):
        """Aj (ba nirdishto ekta tarikhe) habit ta korecho bole mark koro."""
        if name not in self.habits:
            return f"'{name}' bole kono habit nei. Age add_habit diye jog koro."
        day = on_date or date.today().isoformat()
        if day in self.habits[name]:
            return f"'{name}' - {day} tarikhe agei mark kora hoyeche."
        self.habits[name].add(day)
        return f"'{name}' - {day} tarikhe done! Streak: {self.streak(name)} din."

    def streak(self, name, up_to=None):
        """Aj porjonto tana koto din habit ta kora hoyeche (current streak)."""
        if name not in self.habits:
            return 0
        done = self.habits[name]
        day = date.fromisoformat(up_to) if up_to else date.today()
        count = 0
        while day.isoformat() in done:
            count += 1
            day -= timedelta(days=1)
        return count

    def completion_rate(self, name, days=7, up_to=None):
        """Goto koyek dine habit ta kototuku kora hoyeche (shotkora)."""
        if name not in self.habits:
            return 0.0
        done = self.habits[name]
        end = date.fromisoformat(up_to) if up_to else date.today()
        done_days = sum(
            1 for i in range(days)
            if (end - timedelta(days=i)).isoformat() in done
        )
        return round(done_days / days * 100, 1)

    def today_status(self, on_date=None):
        """Aj kon habit done, kon ta baki - ekta summary dao."""
        day = on_date or date.today().isoformat()
        lines = [f"Ajker habit status ({day}):"]
        for name in sorted(self.habits):
            mark = "✅ Done" if day in self.habits[name] else "⬜ Baki"
            lines.append(
                f"  {mark} - {name} (streak: {self.streak(name, up_to=day)} din)"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    tracker = HabitTracker()

    # Uddahoron 1: koyekta rojkar habit jog kora
    print(tracker.add_habit("Sokale hata"))
    print(tracker.add_habit("Boi pora"))
    print(tracker.add_habit("Pani 8 glass"))
    print()

    # Uddahoron 2: goto 3 diner check-in diye streak dekha
    for i in range(3, 0, -1):
        day = (date.today() - timedelta(days=i)).isoformat()
        tracker.check_in("Sokale hata", on_date=day)
    print(tracker.check_in("Sokale hata"))  # ajker check-in
    print(tracker.check_in("Boi pora"))
    print(f"Sokale hata - goto 7 dine: {tracker.completion_rate('Sokale hata')}%")
    print()
    print(tracker.today_status())

    # Uddahoron 3: ekta habit miss hole streak kemon hoy
    tracker.check_in("Pani 8 glass", on_date=(date.today() - timedelta(days=2)).isoformat())
    print()
    print("Pani 8 glass - streak:", tracker.streak("Pani 8 glass"), "din (aj miss, tai 0)")
