import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# main window setup
class SignalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Signals and Systems')
        self.geometry('800x600')

        # signals with their parameters
        self.signals = {
            "Rectangular Signal": ["T", "td"],
            "Triangular Signal": ["T", "td"],
            "Sine Signal": ["A", "f", "td"],
            "Cosine Signal": ["A", "f", "td"],
            "Complex Exponential Signal": ["alpha", "td"],
            "Raised Cosine Signal": ["A", "alpha", "T", "td"],
            "Sinc Signal": ["A", "td"],
            "Unilateral Exponential Signal": ["A", "alpha", "td"],
            "Gaussian Signal": ["A", "sigma", "td"],
            "Constant Unit Signal": ["A", "td"],
            "Dirac Delta Signal": ["td"]
        }

        # create label and buttons for signals
        label = ttk.Label(self, text='Select a Signal:', anchor='center')
        label.pack(pady=10)

        for signal_name in self.signals:
            button = ttk.Button(self, text=signal_name, command=lambda s=signal_name: self.open_signal_window(s))
            button.pack(pady=5)

    # open the signal window
    def open_signal_window(self, signal_name):
        self.params_window = ParamWindow(self, signal_name, self.signals[signal_name], self.plot_signal)
        self.params_window.grab_set()

    # show the signal plot
    def plot_signal(self, signal_name, param_values):
        self.plot_window = PlotWindow(self, signal_name, param_values)
        self.plot_window.grab_set()


# window to input parameters
class ParamWindow(tk.Toplevel):
    def __init__(self, parent, signal_name, params, plot_callback):
        super().__init__(parent)
        self.signal_name = signal_name
        self.params = params
        self.plot_callback = plot_callback
        self.param_inputs = {}

        self.title(f'{self.signal_name} - Input Parameters')
        self.geometry('400x300')

        # input fields for parameters
        for param in self.params:
            label = ttk.Label(self, text=f"Enter {param}:")
            label.pack(pady=5)
            input_field = ttk.Entry(self)
            input_field.pack(pady=5)
            self.param_inputs[param] = input_field

        # button to generate the signal
        plot_button = ttk.Button(self, text='Generate Signal', command=self.on_generate_signal)
        plot_button.pack(pady=10)

    # trigger signal plotting
    def on_generate_signal(self):
        param_values = {param: float(input_field.get()) for param, input_field in self.param_inputs.items()}
        self.plot_callback(self.signal_name, param_values)
        self.destroy()


# window for showing the plot
class PlotWindow(tk.Toplevel):
    def __init__(self, parent, signal_name, param_values):
        super().__init__(parent)
        self.signal_name = signal_name
        self.param_values = param_values

        self.title(f'{self.signal_name} - Signal Plot')
        self.geometry('1200x800')

        self.generate_signal()

    # create the signal
    def generate_signal(self):
        t = np.linspace(-50, 50, 1000)
        td = self.param_values.get("td", 0)
        t_shifted = t - td

        signal = np.zeros_like(t_shifted)

        if self.signal_name == "Sine Signal":
            A = self.param_values["A"]
            f = self.param_values["f"]
            signal = A * np.sin(2 * np.pi * f * t_shifted)
        elif self.signal_name == "Cosine Signal":
            A = self.param_values["A"]
            f = self.param_values["f"]
            signal = A * np.cos(2 * np.pi * f * t_shifted)
        elif self.signal_name == "Rectangular Signal":
            T = self.param_values["T"]
            signal = np.where(np.abs(t_shifted) <= T / 2, 1, 0)
        elif self.signal_name == "Triangular Signal":
            T = self.param_values["T"]
            signal = np.maximum(0, (1 - np.abs(t_shifted) / T))
        elif self.signal_name == "Complex Exponential Signal":
            alpha = self.param_values["alpha"]
            signal = np.exp(alpha * t_shifted)
        elif self.signal_name == "Raised Cosine Signal":
            A = self.param_values["A"]
            alpha = self.param_values["alpha"]
            T = self.param_values["T"]
            signal = A * (1 + np.cos(2 * np.pi * t_shifted / T)) / (1 - (2 * alpha * t_shifted / T) ** 2)
        elif self.signal_name == "Sinc Signal":
            A = self.param_values["A"]
            signal = A * np.sinc(t_shifted)
        elif self.signal_name == "Unilateral Exponential Signal":
            A = self.param_values["A"]
            alpha = self.param_values["alpha"]
            signal = A * np.exp(-alpha * t_shifted) * (t_shifted >= 0)
        elif self.signal_name == "Gaussian Signal":
            A = self.param_values["A"]
            sigma = self.param_values["sigma"]
            signal = A * np.exp(-t_shifted ** 2 / (2 * sigma ** 2))
        elif self.signal_name == "Constant Unit Signal":
            A = self.param_values["A"]
            signal = A * np.ones_like(t_shifted)
        elif self.signal_name == "Dirac Delta Signal":
            signal = np.zeros_like(t_shifted)
            signal[np.abs(t_shifted) < 0.01] = 1

        # plot the signal
        fig, ax = plt.subplots()
        ax.plot(t, signal)

        # set x-axis range and ticks
        ax.set_xlim([-20, 20])
        ax.set_xticks(np.arange(-21, 21, 1))

        ax.set_title(f"{self.signal_name} (Shifted by td = {td})")
        ax.set_xlabel('t')
        ax.set_ylabel('Amplitude')
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# run the app
if __name__ == '__main__':
    app = SignalApp()
    app.mainloop()
