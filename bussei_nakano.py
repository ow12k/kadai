import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


class GrapheneBand:
    t = -3.033  # 最近接原子間のトランスファー積分
    a = 2.461  # 基本格子ベクトルaの大きさ
    b = (4 * np.pi) / (np.sqrt(3) * a)  # 逆格子ベクトルbの大きさ
    width = b  # グラフの幅(今回は第一ブリルアンゾーン全体を含む範囲であるため)

    # バンドギャップ式のルート内部
    def f(self, x: np.ndarray | float, y: np.ndarray | float) -> np.ndarray | float:
        ret = 1 + 4 * np.cos(np.sqrt(3) * x * self.a / 2) * np.cos(y * self.a / 2) + 4 * np.cos(y * self.a / 2) ** 2
        return np.abs(ret) 

    # プラスマイナスの分岐込み式定義
    def E_g(self, x: np.ndarray | float, y: np.ndarray | float, sign: str) -> np.ndarray | float:
        f = self.f(x, y)
        if sign == '+':
            return self.t * np.sqrt(f)
        if sign == '-':
            return -self.t * np.sqrt(f)
        print('wrong sign. sign should be "+" or "-".')
        return -1 


    def plot(self, n: int = 200):
        # プロットの設定
        plt.rcParams["font.size"] = 10
        plt.rcParams["font.family"] = 'Times New Roman'
        rc('mathtext', **{'rm': 'serif', 'fontset': 'cm'})
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d', facecolor='w')
        # 3Dプロット計算
        kx = np.linspace(-self.width, self.width, n)
        ky = np.linspace(-self.width, self.width, n)
        kx, ky = np.meshgrid(kx, ky)
        eg_plus = self.E_g(kx, ky, '+')
        eg_minus = self.E_g(kx, ky, '-')
        ax.plot_surface(kx, ky, eg_plus, zorder=1, cmap='plasma', vmax=15, vmin=-10)
        ax.plot_surface(kx, ky, eg_minus, zorder=2, cmap='plasma', vmax=15, vmin=-10)
        # ブリルアンゾーンの描画設定
        line = np.zeros(4)
        lines_x = [self.b / 2, 0, -1 * self.b / 2, -1 * self.b / 2, 0, self.b / 2]
        lines_y = [self.width / 2 / np.sqrt(3), self.width / np.sqrt(3), self.width / 2 / np.sqrt(3), -1 * self.width / 2 / np.sqrt(3), -1 * self.width / np.sqrt(3), -1 * self.width / 2 / np.sqrt(3)]
        labels = ['Γ', 'M', 'K’', 'K']
        points_x = [0, self.b / 2, self.b / 2, 0]
        points_y = [0, 0, self.width / 2 / np.sqrt(3), self.width / np.sqrt(3)]
        for i in range(6):
            x_tmp = np.linspace(lines_x[i - 1], lines_x[i], 4)
            y_tmp = np.linspace(lines_y[i - 1], lines_y[i], 4)
            ax.plot(x_tmp, y_tmp, line, '-', zorder=3, color='k', linewidth=2)
        for label, x, y in zip(labels, points_x, points_y):
            z = self.E_g(x, y, '+')
            ax.plot(x, y, z, 'o', color='k', zorder=4)
            ax.text(x, y, z + 1, label, zorder=5, fontdict={'family': 'Arial'})
        # 軸ラベル
        ax.set_xlabel(r'$\rm k_{x}$')
        ax.set_ylabel(r'$\rm k_{y}$')
        ax.set_zlabel('$E$  [eV]')
        ax.set_xticks(np.linspace(-self.width, self.width, 5))
        ax.set_yticks(np.linspace(-self.width, self.width, 5))
        ax.set_zticks(np.linspace(-10, 15, 6))
        plt.show()


def main():
    b = GrapheneBand()
    b.plot()


if __name__ == '__main__':
    main()