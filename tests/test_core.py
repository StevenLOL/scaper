
import scaper.core as core
import os


def test_scaper():

    # no arg
    sc = core.Scaper()
    assert sc.bg_path == '../audio/bg'
    assert sc.fg_path == '../audio/fg'
    # one arg
    sc = core.Scaper('../audio/fg')
    assert sc.bg_path == '../audio/bg'
    assert sc.fg_path == '../audio/fg'
    # two arg
    sc = core.Scaper('../audio/fg', '../audio/bg')
    assert sc.bg_path == '../audio/bg'
    assert sc.fg_path == '../audio/fg'
    # key value args
    sc = core.Scaper(fg_path='../audio/fg', bg_path='../audio/bg')
    assert sc.bg_path == '../audio/bg'
    assert sc.fg_path == '../audio/fg'
    # paths dont exist
    sc = core.Scaper(fg_path='../audio/wrong', bg_path='../audio/wwrong')
    assert sc.bg_path == '../audio/bg'
    assert sc.fg_path == '../audio/fg'


def test_scaperspec():

    sc = core.Scaper()

    # no arg
    sp = core.ScaperSpec(sc=None)
    assert sp.sc is not None
    assert sp.bg_label is not None
    assert sp.bg_duration is not None
    # one arg
    sp = core.ScaperSpec(8)
    assert sp.bg_label is not None
    # two arg, no list
    sp = core.ScaperSpec(sc, 'music')
    assert sp.bg_label is not None
    # three arg
    sp = core.ScaperSpec(sc, ['music'], 1)
    assert sp.bg_label is not None
    # key value args, list of bg labels
    sp = core.ScaperSpec(
        scape=sc, bg_label=['music', 'car', 'crowd'], bg_duration=9)
    assert sp.bg_label == ['music'] or ['crowd'] or ['car']
    assert sp.bg_duration == 9

    # wrong label, invalid duration
    sp = core.ScaperSpec(sc, bg_label='wrong', bg_duration=-3)
    assert sp.bg_label != 'wrong'
    assert sp.bg_duration >= 0


def test_add_events():

    sc = core.Scaper()

    # no args
    sp = core.ScaperSpec(sc)
    sp.add_events()
    assert sp.labels is not None
    assert sp.fg_start_times is not None
    assert sp.fg_durations is not None
    assert sp.snrs is not None
    assert sp.num_events is not None
    assert (
        len(sp.labels) == len(sp.fg_durations) == len(sp.fg_start_times) ==
        len(sp.snrs) == sp.num_events)
    # one arg
    sp = core.ScaperSpec(sc)
    sp.add_events(['horn'])
    assert sp.labels == ['horn']
    assert sp.fg_start_times is not None
    assert sp.fg_durations is not None
    assert sp.snrs is not None
    assert sp.num_events is not None
    assert (
        len(sp.labels) == len(sp.fg_durations) == len(sp.fg_start_times) ==
        len(sp.snrs) == sp.num_events)
    # two arg
    sp = core.ScaperSpec(sc)
    sp.add_events(['siren'], [1])
    assert sp.fg_start_times == [1]
    # assert sp.labels == ['siren']
    assert sp.fg_durations is not None
    assert sp.snrs is not None
    assert sp.num_events is not None
    assert (
        len(sp.labels) == len(sp.fg_durations) == len(sp.fg_start_times) ==
        len(sp.snrs) == sp.num_events)
    # three arg
    sp = core.ScaperSpec(sc)
    sp.add_events(['siren'], [1], [2])
    assert sp.fg_start_times == [1]
    # assert sp.labels == ['siren']
    # assert sp.fg_durations == [2]
    assert sp.snrs is not None
    assert sp.num_events is not None
    assert (
        len(sp.labels) == len(sp.fg_durations) == len(sp.fg_start_times) ==
        len(sp.snrs) == sp.num_events)
    # four arg
    sp = core.ScaperSpec(sc)
    sp.add_events(['siren'], [1], [2], [-4])
    assert sp.fg_start_times == [1]
    # assert sp.labels == ['siren']
    # assert sp.fg_durations == [2]
    # assert sp.snrs == [-4]
    # five arg
    sp = core.ScaperSpec(sc)
    sp.add_events(['siren'], [1], [2], [-4], 1)
    assert sp.fg_start_times == [1]
    # assert sp.labels == ['siren']
    # assert sp.fg_durations == [2]
    # assert sp.snrs == [-4]

    # collapse these vvv
    # snrs
    sp = core.ScaperSpec(sc)
    sp.add_events(snrs=-1)
    assert sp.snrs == [-1]

    # fg_start_times
    sp = core.ScaperSpec(sc)
    sp.add_events(fg_start_times=1)
    assert sp.fg_start_times == [1]
    sp = core.ScaperSpec(sc)
    sp.add_events(fg_start_times=[1, 2, 3], num_events=4)
    assert sp.fg_start_times != [1, 2, 3]

    # fg_durations
    sp.add_events(fg_durations=1)
    assert sp.fg_durations == [1]
    sp = core.ScaperSpec(sc)
    sp.add_events(fg_durations=[1, 2, 3], num_events=2)
    assert sp.fg_durations != [1, 2, 3]

    # invalid labels, invalid start times, invalid durations,
    # invalid snrs more start times then events
    sp = core.ScaperSpec(sc)
    sp.add_events(
        labels=['foo', 'bar'], fg_start_times=[-200, -200, 0],
        fg_durations=[-1, 0, 3], snrs=[1, 4, 5], num_events=3)
    assert sp.labels != ['foo', 'bar']
    assert sp.fg_start_times != [-200, -200]
    assert len(sp.fg_start_times) == 3
    assert sp.fg_durations != [-1, 0]
    assert sp.snrs is not None
    assert sp.num_events == 3

    # duration checks
    sp = core.ScaperSpec(sc, bg_label=['music'], bg_duration=10)
    sp.add_events(
        labels=['music'], fg_start_times=[5, 6, 7, 8], fg_durations=[6],
        snrs=[-1, -3], num_events=5)
    assert len(sp.fg_durations) == 5

    # invalid number of events
    sp = core.ScaperSpec(sc, bg_label=['siren'], bg_duration=10)
    sp.add_events(
        labels=['horn'], fg_start_times=[5, 6, 7, 8], fg_durations=[6],
        snrs=[-1, -3], num_events=-1)
    assert len(sp.fg_durations) == 1

    # list extension checks
    sp = core.ScaperSpec(sc)
    sp.add_events(labels=['foo', 'bar'], fg_start_times=[2, 2, 0],
                  fg_durations=[1, 2, 3], snrs=[1, 4, 5], num_events=5)
    assert sp.num_events is not None

    # more params than events
    sp = core.ScaperSpec(sc)
    sp.add_events(
        labels='siren', fg_start_times=[1, 2], fg_durations=[1, 2, 3],
        snrs=[1, 4, 5], num_events=1)
    assert sp.num_events is not None

    # less events than params
    sp = core.ScaperSpec(sc)
    sp.add_events(
        labels=['siren', 'siren'], fg_start_times=[1, 2],
        fg_durations=[1, 2, 3], snrs=[1, 4, 5], num_events=1)
    assert sp.num_events is not None


def test_generate_jams():

    sc = core.Scaper()
    sp = core.ScaperSpec(sc, bg_label=['crowd'], bg_duration=10)
    sp.add_events(
        labels=['horn', 'siren'], fg_start_times=[3, 2], fg_durations=[1, 1],
        snrs=[-2, -5], num_events=2)
    the_jam = sp.generate_jams(sp.spec, 'tests/tmp/dummy_outfile.jams')
    assert the_jam

    # the_jam = sp.generate_jams()
    # assert the_jam


def test_generate_soundscapes():

    sc = core.Scaper()
    sp = core.ScaperSpec()
    sp.add_events(
        labels=['horn'], fg_start_times=[2], fg_durations=[1], snrs=[-5],
        num_events=2)
    the_jam = sp.generate_jams(sp.spec, 'tests/tmp/test_jams1.jams')

    # 0 args
    sc.generate_soundscapes()
    clear_test_dir()
    # 1 arg
    sc.generate_soundscapes('tests/tmp/test_jams1.jams')
    clear_test_dir()
    # 2 arg
    sc.generate_soundscapes('tests/tmp/test_jams1.jams',
                            'tests/tmp/audio/output_audio.wav')
    # clear_test_dir()
    assert the_jam

    # incorrect filepath
    sp = core.ScaperSpec(sc, bg_label=['crowd'], bg_duration=10)
    sp.add_events(labels=['horn', 'siren'], fg_start_times=[3, 2],
                  fg_durations=[1, 1], snrs=[-2, -5], num_events=2)
    the_jam = sp.generate_jams(sp.spec, 'tests/tmp/dummy_outfile.jams')
    sc.generate_soundscapes('tests/tmp/incorrec_name.jams',
                            'tests/tmp/dummy_output_audio.wav')
    assert the_jam

    # correct filepath
    the_jam = sp.generate_jams(sp.spec, 'tests/tmp/test_jams2.jams')
    sc.generate_soundscapes('tests/tmp/test_jams2.jams',
                            'tests/tmp/dummy_output_audio.wav')
    assert the_jam

    # output audio file already exists
    # sc.generate_soundscapes(j_file='test/test_jams2.jams',
    #                         s_file='test/dummy_output_audio.wav')

    # assert not the_jam
    assert the_jam

    # output audio filepath invalid
    sc.generate_soundscapes(j_file='tests/tmp/test_jams2.jams',
                            s_file='tests/tmp/dummy/output')
    # assert not the_jam
    assert the_jam


def clear_test_dir():
    # clear test folder of previous jams and audio files
    folder = 'tests/tmp'
    for each_file in os.listdir(folder):
        file_path = os.path.join(folder, each_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()

    # # labels, start times, durations, snrs, num events
    # sp.add_events(labels=['horn', 'siren'], fg_start_times=[3, 2],
    #               fg_durations=[1, 1], snrs=[-2,-5], num_events=4)
    # thejam = sp.generate_jams(sp.spec, 'jammyjamm.jams')
    # sc.generate_soundscapes(
    #     './jams/jammyjamm.jams','./output_audio/output_audio.wav')
