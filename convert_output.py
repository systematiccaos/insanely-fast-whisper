import argparse
import json
import os


class TxtFormatter:
    @classmethod
    def preamble(cls):
        return ""

    @classmethod
    def format_chunk(cls, chunk, index):
        text = chunk['text']
        return f"{text}\n"


class SrtFormatter:
    @classmethod
    def preamble(cls):
        return ""

    @classmethod
    def format_seconds(cls, seconds):
        whole_seconds = int(seconds)
        milliseconds = int((seconds - whole_seconds) * 1000)

        hours = whole_seconds // 3600
        minutes = (whole_seconds % 3600) // 60
        seconds = whole_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    @classmethod
    def format_chunk(cls, chunk, index):
        text = chunk['text']
        speaker = chunk['speaker']
        colors = {
            'SPEAKER_00': '#ff00ff',
            'SPEAKER_01': '#ff0000',
            'SPEAKER_02': '#ff1800',
            'SPEAKER_03': '#ff3000',
            'SPEAKER_04': '#ff4800',
            'SPEAKER_05': '#ff6000',
            'SPEAKER_06': '#ff7800',
            'SPEAKER_07': '#ff8f00',
            'SPEAKER_08': '#ffa700',
            'SPEAKER_09': '#ffbf00',
            'SPEAKER_10': '#ffd700',
            'SPEAKER_11': '#ffef00',
            'SPEAKER_12': '#f7ff00',
            'SPEAKER_13': '#dfff00',
            'SPEAKER_14': '#c7ff00',
            'SPEAKER_15': '#afff00',
            'SPEAKER_16': '#97ff00',
            'SPEAKER_17': '#7fff00',
            'SPEAKER_18': '#68ff00',
            'SPEAKER_19': '#50ff00',
            'SPEAKER_20': '#38ff00',
            'SPEAKER_21': '#20ff00',
            'SPEAKER_22': '#08ff00',
            'SPEAKER_23': '#00ff10',
            'SPEAKER_24': '#00ff28',
            'SPEAKER_25': '#00ff40',
            'SPEAKER_26': '#00ff58',
            'SPEAKER_27': '#00ff70',
            'SPEAKER_28': '#00ff87',
            'SPEAKER_29': '#00ff9f',
            'SPEAKER_30': '#00ffb7',
            'SPEAKER_31': '#00ffcf',
            'SPEAKER_32': '#00ffe7',
            'SPEAKER_33': '#00ffff',
            'SPEAKER_34': '#00e7ff',
            'SPEAKER_35': '#00cfff',
            'SPEAKER_36': '#00b7ff',
            'SPEAKER_37': '#009fff',
            'SPEAKER_38': '#0087ff',
            'SPEAKER_39': '#0070ff',
            'SPEAKER_40': '#0058ff',
            'SPEAKER_41': '#0040ff',
            'SPEAKER_42': '#0028ff',
            'SPEAKER_43': '#0010ff',
            'SPEAKER_44': '#0800ff',
            'SPEAKER_45': '#2000ff',
            'SPEAKER_46': '#3800ff',
            'SPEAKER_47': '#5000ff',
            'SPEAKER_48': '#6800ff',
            'SPEAKER_49': '#7f00ff',
            'SPEAKER_50': '#9700ff',
            'SPEAKER_51': '#af00ff',
            'SPEAKER_52': '#c700ff',
            'SPEAKER_53': '#df00ff',
            'SPEAKER_54': '#f700ff',
            'SPEAKER_55': '#ff00ef',
            'SPEAKER_56': '#ff00d7',
            'SPEAKER_57': '#ff00bf',
            'SPEAKER_58': '#ff00a7',
            'SPEAKER_59': '#ff008f',
            'SPEAKER_60': '#ff0078',
            'SPEAKER_61': '#ff0060',
            'SPEAKER_62': '#ff0048',
            'SPEAKER_63': '#ff0030',
            'SPEAKER_64': '#ff0018'
        }

        start, end = chunk['timestamp'][0], chunk['timestamp'][1]
        start_format, end_format = cls.format_seconds(start), cls.format_seconds(end)
        return f"{index}\n{start_format} --> {end_format}\n<font color=\"{colors[speaker]}\" data-speaker=\"{speaker}\">{text}</font>\n\n"


class VttFormatter:
    @classmethod
    def preamble(cls):
        return "WEBVTT\n\n"

    @classmethod
    def format_seconds(cls, seconds):
        whole_seconds = int(seconds)
        milliseconds = int((seconds - whole_seconds) * 1000)

        hours = whole_seconds // 3600
        minutes = (whole_seconds % 3600) // 60
        seconds = whole_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    @classmethod
    def format_chunk(cls, chunk, index):
        text = chunk['text']
        start, end = chunk['timestamp'][0], chunk['timestamp'][1]
        start_format, end_format = cls.format_seconds(start), cls.format_seconds(end)
        return f"{index}\n{start_format} --> {end_format}\n{text}\n\n"


def convert(input_path, output_format, output_dir, verbose):
    with open(input_path, 'r') as file:
        data = json.load(file)

    formatter_class = {
        'srt': SrtFormatter,
        'vtt': VttFormatter,
        'txt': TxtFormatter
    }.get(output_format)

    string = formatter_class.preamble()
    for index, chunk in enumerate(data['speakers'], 1):
        entry = formatter_class.format_chunk(chunk, index)

        if verbose:
            print(entry)

        string += entry

    with open(os.path.join(output_dir, f"output.{output_format}"), 'w', encoding='utf-8') as file:
        file.write(string)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON to an output format.")
    parser.add_argument("input_file", help="Input JSON file path")
    parser.add_argument("-f", "--output_format", default="all", help="Format of the output file (default: srt)", choices=["txt", "vtt", "srt"])
    parser.add_argument("-o", "--output_dir", default=".", help="Directory where the output file/s is/are saved")
    parser.add_argument("--verbose", action="store_true", help="Print each VTT entry as it's added")

    args = parser.parse_args()
    convert(args.input_file, args.output_format, args.output_dir, args.verbose)

if __name__ == "__main__":
    # Example Usage:
    # python convert_output.py output.json -f vtt -o /tmp/my/output/dir
    main()
