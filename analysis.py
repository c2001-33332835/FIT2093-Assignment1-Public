from encryption import encrypt, decrypt
from matplotlib import pyplot as plt

MESSAGES = 0x8ba3
KEYS = [0x19,0x17,0x3F,0x68,0xCE]
COLOR = ["darkorange","yellowgreen", "dodgerblue", "mediumorchid"]

def get_hex_digit(n, digit):
  return (n >> (digit * 4)) & 0xF

def get_encryption(message, key, digit):
  result = []

  for i in range(0x0, 0x10 ** (digit + 1), 0x10 ** digit):
    m = message + i
    result.append(encrypt(m, key))

  return result

def get_plot_data(items):
  return [[(i, get_hex_digit(x, n)) for i, x in enumerate(items)] for n in range(4)]

def plot_data(data, title="", filename="fig.png"):
  plt.clf()
  plt.close()
  plt.title(title)
  plt.xlabel("x")
  plt.ylabel("result when encrypted with $m$")
  plt.xticks(list(range(16)), [hex(x)[2].upper() for x in range(16)])
  plt.yticks(list(range(16)), [hex(x)[2].upper() for x in range(16)])

  legend = []

  for digit, digit_data in enumerate(data):
    # plot points
    for hex_val, result in digit_data:
      plt.plot(hex_val, result, color=COLOR[digit], markersize="3", marker="o")

    x = [x for x, _ in digit_data]
    y = [y for _, y in digit_data]
    l, = plt.plot(x, y, color=COLOR[digit])
    legend.append(l)

  plt.legend(legend, [f"{nth} digit" for nth in ["1st", "2nd", "3rd", "4th"]])
  plt.grid()
  plt.savefig(filename)
  # plt.show()
  print(f"Generated {filename}")

def purge_digit(n, digit):
  return ((0xF << digit * 4) ^ 0xFFFF) & n

def encrypt_nth_round(message, keys, round, digit):
  chain_input = get_encryption(message, keys[0], digit)
  for i in range(1, round):
    chain_input = [encrypt(m, keys[i]) for m in chain_input]
  
  return chain_input


for d in range(4):
  for round in [0,2,4]:
    message = purge_digit(MESSAGES, d)
    data_0 = get_plot_data(encrypt_nth_round(message, KEYS, round, d))
    label = list(hex(message))
    label[-d - 1] = "$x$"
    if d != 3:
      label[2] = "$" + label[2]
    label = "".join(label)
    plot_data(data_0, title=f"Encryption result with message $m={label[2:]} at round {round + 1}", filename=f"digit_{d}_round_{round}.png")
