class Vehicle:
    def __init__(self, brand: str, model: str, number: str) -> None:
        self.brand = brand
        self.model = model
        self.number = number
        self._available = True

    def show_info(self) -> None:
        print(f"Производитель: {self.brand}")
        print(f"Модель: {self.model}")
        print(f"Номер: {self.number}")
        print(f"Доступен: {self._available}")

    def is_available(self) -> bool:
        return self._available

    def start_rent(self) -> None:
        if not self._available:
            raise ValueError("Транспорт уже арендован")

        self._available = False

    def finish_rent(self) -> None:
        if self._available:
            raise ValueError("Транспорт не находится в аренде")

        self._available = True

    def calculate_price(self, minutes: int) -> float:
        raise NotImplementedError


class Car(Vehicle):
    def __init__(
            self,
            brand: str,
            model: str,
            number: str,
            fuel_type: str,
            price_per_minute: float
    ) -> None:
        super().__init__(brand, model, number)

        self.fuel_type = fuel_type
        self.price_per_minute = price_per_minute

    def calculate_price(self, minutes: int) -> float:
        if not isinstance(minutes, int) or minutes <= 0:
            raise ValueError("Некорректная продолжительность аренды")

        return minutes * self.price_per_minute

    def show_info(self) -> None:
        super().show_info()
        print(f"Тип топлива: {self.fuel_type}")
        print(f"Стоимость минуты: {self.price_per_minute} руб.")


class Scooter(Vehicle):
    def __init__(
            self,
            brand: str,
            model: str,
            number: str,
            battery_level: int,
            price_per_minute: float
    ) -> None:
        super().__init__(brand, model, number)

        self.battery_level = battery_level
        self.price_per_minute = price_per_minute

    def calculate_price(self, minutes: int) -> float:
        if not isinstance(minutes, int) or minutes <= 0:
            raise ValueError("Некорректная продолжительность аренды")

        return 30 + minutes * self.price_per_minute

    def show_info(self) -> None:
        super().show_info()
        print(f"Уровень заряда: {self.battery_level}%")
        print(f"Стоимость минуты: {self.price_per_minute} руб.")


class Bicycle(Vehicle):
    def __init__(
            self,
            brand: str,
            model: str,
            number: str,
            bike_type: str,
            price_per_hour: float
    ) -> None:
        super().__init__(brand, model, number)

        self.bike_type = bike_type
        self.price_per_hour = price_per_hour

    def calculate_price(self, minutes: int) -> float:
        if not isinstance(minutes, int) or minutes <= 0:
            raise ValueError("Некорректная продолжительность аренды")

        hours = (minutes + 59) // 60

        return hours * self.price_per_hour

    def show_info(self) -> None:
        super().show_info()
        print(f"Тип велосипеда: {self.bike_type}")
        print(f"Стоимость часа: {self.price_per_hour} руб.")


class UserAccount:
    def __init__(self, username: str, balance: float) -> None:
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")

        self.username = username
        self._balance = balance

    def get_balance(self) -> float:
        return self._balance

    def top_up(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")

        self._balance += amount

    def pay(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        if amount > self._balance:
            raise ValueError("Недостаточно средств")

        self._balance -= amount


def process_rent(
        user: UserAccount,
        vehicle: Vehicle,
        minutes: int
) -> bool:
    if not vehicle.is_available():
        print("Транспорт уже арендован")
        return False

    try:
        price = vehicle.calculate_price(minutes)
        user.pay(price)
        vehicle.start_rent()

    except ValueError as error:
        print(f"Ошибка: {error}")
        return False

    print("\nАренда успешно оформлена")
    print(f"Пользователь: {user.username}")
    print(f"Транспорт: {vehicle.brand} {vehicle.model}")
    print(f"Стоимость: {price} руб.")
    print(f"Остаток баланса: {user.get_balance()} руб.")

    return True


def main() -> None:
    user = UserAccount("Иван", 1000)

    car1 = Car("Toyota", "Camry", "A001", "Бензин", 12)
    car2 = Car("Kia", "Rio", "A002", "Бензин", 18)

    scooter = Scooter("Xiaomi", "Pro 2", "S001", 80, 5)

    bicycle = Bicycle("Stels", "Navigator", "B001", "Городской", 120)

    vehicles: list[Vehicle] = [
        car1,
        car2,
        scooter,
        bicycle
    ]

    print("СПИСОК ТРАНСПОРТА")

    for vehicle in vehicles:
        print()
        vehicle.show_info()

    print("\nРАСЧЁТ СТОИМОСТИ")
    print(f"Автомобиль: {car1.calculate_price(20)} руб.")
    print(f"Самокат: {scooter.calculate_price(20)} руб.")
    print(f"Велосипед: {bicycle.calculate_price(75)} руб.")
    print("\nАРЕНДА АВТОМОБИЛЯ")
    process_rent(user, car1, 20)

    print("\nПОВТОРНАЯ АРЕНДА")
    process_rent(user, car1, 20)
    print("\nЗАВЕРШЕНИЕ АРЕНДЫ")
    car1.finish_rent()
    print("Транспорт доступен:", car1.is_available())
    print("\nПРОВЕРКА БАЛАНСА")
    process_rent(user, car2, 60)
    print("\nПОПОЛНЕНИЕ БАЛАНСА")
    user.top_up(1000)
    print("Текущий баланс:", user.get_balance())
    print("\nПОВТОРНАЯ ПОПЫТКА АРЕНДЫ")
    process_rent(user, car2, 60)
    print("\nАРЕНДА САМОКАТА")
    process_rent(user, scooter, 20)
    print("\nАРЕНДА ВЕЛОСИПЕДА")
    process_rent(user, bicycle, 75)
    print("\nЗАВЕРШЕНИЕ АРЕНДЫ ВЕЛОСИПЕДА")
    bicycle.finish_rent()
    print("\nПРОВЕРКА НЕКОРРЕКТНОЙ ПРОДОЛЖИТЕЛЬНОСТИ")
    process_rent(user, bicycle, 0)
    process_rent(user, bicycle, -10)


if __name__ == "__main__":
    main()
