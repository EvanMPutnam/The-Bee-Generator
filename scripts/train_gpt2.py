import gpt_2_simple as gpt2

# Config params
TOTAL_STEPS = 220

def train(sess, file_name, run_name, steps = TOTAL_STEPS):
    gpt2.download_gpt2(model_name="124M")
    gpt2.finetune(sess,
                dataset = file_name,
                model_name = '124M',
                steps = TOTAL_STEPS,
                restore_from = 'fresh',
                run_name = run_name,
                print_every = 10,
                sample_every = 200,
                save_every = 20
                )

def generate(iters, file_name, run_name, temperature = 0.7):
    with open(file_name, "w+") as fle:
        for count in range(0, iters):
            data = gpt2.generate(sess,
                    length = 250,
                    temperature = temperature,
                    nsamples = 100,
                    batch_size = 20,
                    run_name = run_name,
                    return_as_list = True
                    )
            for i in range(0, len(data)):
                lines = data[i].split("\n")
                for i2 in range(0, len(lines)-1):
                    fle.write(lines[i2] + '\n')
            print("Count: " + str(count))

def filter_results(results_file, titles_file):
    old_tiles = {}
    with open(titles_file, encoding = "utf-8") as titles:
        for line in titles.readlines():
            old_tiles[line.strip()] = True
    lines_to_write = []
    with open(results_file, encoding = "utf-8") as results:
        for result in results.readlines():
            line = result.strip()
            # Get rid of existing titles, blank titles, and single word titles.
            if line not in old_tiles and line.strip() != "" and len(line.split()) != 1:
                lines_to_write.append(line)
    with open(results_file, "w+", encoding = "utf-8") as new_results:
        for line in lines_to_write:
            new_results.write(line + '\n')
    

if __name__ == "__main__":
    sess = gpt2.start_tf_sess()
    train(sess, "../data/titles.txt", "runT2")
    generate(220, "../data/gpt2_results.txt", "runT2")
    filter_results("../data/gpt2_results.txt", "../data/titles.txt")

