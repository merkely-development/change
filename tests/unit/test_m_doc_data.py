import os
import sys
sys.path.append(os.path.abspath("/app/source"))
import doc_data
from pyfakefs.fake_filesystem_unittest import TestCase


class AutoGenerateReferenceTextFilesTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_auto_generate(self):
        doc_data.auto_generate_txt_files()
        # TODO: assert txt files exist


def test_generate_docs():
    docs = doc_data.generate_docs()
    assert "/docs/build/reference/github/log_test.txt" in docs.keys()


def test_lines_for_command_reference_string():
    doc_data.lines_for('bitbucket', 'log_test')
    doc_data.lines_for('docker', 'log_test')
    doc_data.lines_for('github', 'log_test')


def test_lines_for_minimum_use_string():
    doc_data.min_lines_for('log_test')

