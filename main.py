import arcade
import settings
import nesteplanet


def main():
    """Main function"""
    window = nesteplanet.NestePlanet()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()