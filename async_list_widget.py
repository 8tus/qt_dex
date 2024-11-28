from PyQt6.QtWidgets import QApplication, QListWidget
import asyncio

class AsyncListWidget(QListWidget):
    def __init__(self):
        super().__init__()

    async def load_all_images(self):
        """Carga las imágenes para todos los elementos."""
        tasks = [item.fetch_image() for item in self._iter_items()]
        await asyncio.gather(*tasks)

    def _iter_items(self):
        """Itera sobre los elementos de la lista."""
        for row in range(self.count()):
            yield self.item(row)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Crear la lista y agregar elementos personalizados
    list_widget = AsyncListWidget()
    list_widget.addItem(AsyncListWidgetItem("Bulbasaur", "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"))
    list_widget.addItem(AsyncListWidgetItem("Ivysaur", "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png"))
    list_widget.addItem(AsyncListWidgetItem("Venusaur", "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png"))

    list_widget.show()

    # Cargar imágenes de manera asíncrona
    asyncio.run(list_widget.load_all_images())

    sys.exit(app.exec())
