from libraries.utility import Utility as Util
import os


def main():
    mu = Util()
    dbs_d = os.path.join(mu.get_this_dir(),"dbs")
    m_dict = mu.get_subdirectories_dict(dbs_d,filetype=".sql")


main()
