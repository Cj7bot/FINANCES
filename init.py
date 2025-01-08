import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def obtener_grafico():
    symbol = symbol_entry.get().upper()
    period_choice = period_var.get()

    if period_choice in time_periods:
        months = time_periods[period_choice]
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)

        try:
            data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
            
            if data.empty:
                messagebox.showerror("Error", f"No se encontraron datos para el símbolo {symbol}. Verifique si el símbolo es correcto.")
                return
            
            print("Columnas disponibles:", data.columns)

            if 'Adj Close' in data.columns:
                plt.figure(figsize=(12, 6))
                plt.plot(data.index, data['Adj Close'], label=symbol)
                plt.title(f'Precio de cierre ajustado de {symbol}')
                plt.xlabel('Fecha')
                plt.ylabel('Precio ($)')
                plt.legend()
                plt.grid(True)
                plt.show()
            else:
                if 'Close' in data.columns:
                    plt.figure(figsize=(12, 6))
                    plt.plot(data.index, data['Close'], label=symbol)
                    plt.title(f'Precio de cierre de {symbol}')
                    plt.xlabel('Fecha')
                    plt.ylabel('Precio ($)')
                    plt.legend()
                    plt.grid(True)
                    plt.show()
                else:
                    messagebox.showerror("Error", "No se encontraron columnas adecuadas para graficar los precios.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al obtener los datos: {e}")
    else:
        messagebox.showerror("Error", "Periodo de tiempo inválido. Elija entre 6 meses, 1 año o 2 años.")

time_periods = {
    "6 meses": 6,
    "1 año": 12,
    "2 años": 24
}

root = tk.Tk()
root.title("Gráfico de Precios de Acciones")

title_label = tk.Label(root, text="Obtener gráfico de precios de acciones", font=("Arial", 16))
title_label.pack(pady=10)

symbol_label = tk.Label(root, text="Ingrese el símbolo de la empresa (Ejemplo: AAPL para Apple):")
symbol_label.pack(pady=5)

symbol_entry = tk.Entry(root, width=20)
symbol_entry.pack(pady=5)

period_label = tk.Label(root, text="Seleccione el período de tiempo:")
period_label.pack(pady=5)

period_var = tk.StringVar(value="6 meses")

period_menu = tk.OptionMenu(root, period_var, "6 meses", "1 año", "2 años")
period_menu.pack(pady=5)

grafico_button = tk.Button(root, text="Obtener gráfico", command=obtener_grafico)
grafico_button.pack(pady=10)

root.mainloop()
