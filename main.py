import arcade
import settings
import nesteplanet


def main():
    """Main function"""
    window = nesteplanet.NestePlanet()
    window.setup()
    arcade.run()

#testset
if __name__ == "__main__":
    main()