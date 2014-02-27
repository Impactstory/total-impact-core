from test.unit_tests.providers import common
from test.unit_tests.providers.common import ProviderTestCase
from test.utils import http
from totalimpact.providers.provider import Provider, ProviderItemNotFoundError

import os
from nose.tools import assert_equals, assert_items_equal, raises, nottest
import collections

datadir = os.path.join(os.path.split(__file__)[0], "../../../extras/sample_provider_pages/orcid")
SAMPLE_EXTRACT_MEMBER_ITEMS_PAGE = os.path.join(datadir, "members")
SAMPLE_EXTRACT_MEMBER_ITEMS_PAGE2 = os.path.join(datadir, "members2")
SAMPLE_EXTRACT_MEMBER_ITEMS_PAGE3 = os.path.join(datadir, "members3")

TEST_ORCID_ID = "0000-0003-1613-5981"
TEST_ORCID_ID2 = "0000-0001-9107-0714"
TEST_ORCID_ID3 = "0000-0002-3127-3891"
# test curl -H "Accept: application/orcid+json" htid.org/0000-0001-9107-0714/orcid-works

SAMPLE_EXTRACT_MEMBER_ITEMS_SHORT = """
<orcid-work put-code="5177473">
                    <work-title>
                        <title>The Bioperl toolkit: Perl modules for the life sciences</title>
                        <subtitle>Genome Research</subtitle>
                    </work-title>
                    <work-citation>
                        <work-citation-type>bibtex</work-citation-type>
                        <citation>@article{lapp2002,
    volume  = {12},
    number  = {10},
    pages   = {1611-1618},
}
</citation>
                    </work-citation>
                    <publication-date>
                        <year>2002</year>
                    </publication-date>
                    <url>http://www.scopus.com/inward/record.url?eid=2-s2.0-18644368714&amp;partnerID=MN8TOARS</url>
                    <work-source>NOT_DEFINED</work-source>
                </orcid-work>
"""

class TestOrcid(ProviderTestCase):

    provider_name = "orcid"

    testitem_members = TEST_ORCID_ID

    def setUp(self):
        ProviderTestCase.setUp(self)
    
    def test_extract_members(self):
        f = open(SAMPLE_EXTRACT_MEMBER_ITEMS_PAGE, "r")
        members = self.provider._extract_members(f.read(), TEST_ORCID_ID)
        print members
        expected = [('doi', '10.1038/493159a'), ('doi', '10.1038/493159a'), ('doi', '10.6084/m9.figshare.92959'), ('doi', '10.1038/473285a'), ('doi', '10.1002/meet.14504701421'), ('doi', '10.1002/meet.14504701413'), ('doi', '10.1002/meet.2011.14504801337'), ('doi', '10.1002/meet.2011.14504801337'), ('doi', '10.1525/bio.2011.61.8.8'), ('doi', '10.1525/bio.2011.61.8.8'), ('doi', '10.1038/473285a'), ('doi', '10.1038/473285a'), ('doi', '10.5061/dryad.j1fd7'), ('doi', '10.1371/journal.pone.0018537'), ('doi', '10.1371/journal.pone.0018537'), ('doi', '10.1002/meet.2011.14504801327'), ('doi', '10.1002/meet.2011.14504801327'), ('doi', '10.1002/meet.2011.14504801205'), ('doi', '10.1002/meet.2011.14504801205'), ('doi', '10.1371/journal.pone.0018657'), ('doi', '10.1371/journal.pone.0018657'), ('doi', '10.1038/npre.2010.5452.1'), ('doi', '10.1016/j.joi.2009.11.010'), ('doi', '10.1038/npre.2010.4267.1'), ('doi', '10.1002/meet.14504701450'), ('doi', '10.1002/meet.14504701450'), ('doi', '10.1002/meet.14504701445'), ('doi', '10.1002/meet.14504701445'), ('doi', '10.1002/meet.14504701421'), ('doi', '10.1002/meet.14504701421'), ('doi', '10.1016/j.joi.2009.11.010'), ('doi', '10.1016/j.joi.2009.11.010'), ('doi', '10.1002/meet.14504701413'), ('doi', '10.1002/meet.14504701413'), ('doi', '10.1038/npre.2008.2152.1'), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {A review of journal policies for sharing research data},\n\tjournal = {Open Scholarship: Authority, Community, and Sustainability in the Age of Web 2.0 - Proceedings of the 12th International Conference on Electronic Publishing, ELPUB 2008},\n\tyear = {2008},\n\tpages = {1-14},\n\tauthor = {Piwowar, H.A. and Chapman, W.W.}\n}\n\n', 'title': 'A review of journal policies for sharing research data', 'first_author': u'Piwowar', 'journal': 'Open Scholarship: Authority, Community, and Sustainability in the Age of Web 2.0 - Proceedings of the 12th International Conference on Electronic Publishing, ELPUB 2008', 'year': '2008', 'number': '', 'volume': '', 'first_page': '1-14', 'authors': u'Piwowar, Chapman', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {A review of journal policies for sharing research data},\n\tjournal = {Open Scholarship: Authority, Community, and Sustainability in the Age of Web 2.0 - Proceedings of the 12th International Conference on Electronic Publishing, ELPUB 2008},\n\tyear = {2008},\n\tpages = {1-14},\n\tauthor = {Piwowar, H.A. and Chapman, W.W.}\n}\n\n', 'title': 'A review of journal policies for sharing research data', 'first_author': u'Piwowar', 'journal': 'Open Scholarship: Authority, Community, and Sustainability in the Age of Web 2.0 - Proceedings of the 12th International Conference on Electronic Publishing, ELPUB 2008', 'year': '2008', 'number': '', 'volume': '', 'first_page': '1-14', 'authors': u'Piwowar, Chapman', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {Envisioning a biomedical data reuse registry.},\n\tjournal = {AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium},\n\tyear = {2008},\n\tauthor = {Piwowar, H.A. and Chapman, W.W.}\n}\n\n', 'title': 'Envisioning a biomedical data reuse registry.', 'first_author': u'Piwowar', 'journal': 'AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium', 'year': '2008', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Piwowar, Chapman', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {Envisioning a biomedical data reuse registry.},\n\tjournal = {AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium},\n\tyear = {2008},\n\tauthor = {Piwowar, H.A. and Chapman, W.W.}\n}\n\n', 'title': 'Envisioning a biomedical data reuse registry.', 'first_author': u'Piwowar', 'journal': 'AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium', 'year': '2008', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Piwowar, Chapman', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {Identifying data sharing in biomedical literature.},\n\tjournal = {AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium},\n\tyear = {2008},\n\tpages = {596-600},\n\tauthor = {Piwowar, H.A. and Chapman, W.W.}\n}\n\n', 'title': 'Identifying data sharing in biomedical literature.', 'first_author': u'Piwowar', 'journal': 'AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium', 'year': '2008', 'number': '', 'volume': '', 'first_page': '596-600', 'authors': u'Piwowar, Chapman', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {Identifying data sharing in biomedical literature.},\n\tjournal = {AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium},\n\tyear = {2008},\n\tpages = {596-600},\n\tauthor = {Piwowar, H.A. and Chapman, W.W.}\n}\n\n', 'title': 'Identifying data sharing in biomedical literature.', 'first_author': u'Piwowar', 'journal': 'AMIA ... Annual Symposium proceedings / AMIA Symposium. AMIA Symposium', 'year': '2008', 'number': '', 'volume': '', 'first_page': '596-600', 'authors': u'Piwowar, Chapman', 'full_citation_type': 'bibtex'}), ('doi', '10.1371/journal.pmed.0050183'), ('doi', '10.1371/journal.pmed.0050183'), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {Towards a data sharing culture: recommendations for leadership from academic health centers.},\n\tjournal = {PLoS medicine},\n\tyear = {2008},\n\tvolume = {5},\n\tnumber = {9},\n\tauthor = {Piwowar, H.A. and Becich, M.J. and Bilofsky, H. and Crowley, R.S.}\n}\n\n', 'title': 'Towards a data sharing culture: recommendations for leadership from academic health centers.', 'first_author': u'Piwowar', 'journal': 'PLoS medicine', 'year': '2008', 'number': '9', 'volume': '5', 'first_page': '', 'authors': u'Piwowar, Becich, Bilofsky, Crowley', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article { piwowar2008,\n\ttitle = {Towards a data sharing culture: recommendations for leadership from academic health centers.},\n\tjournal = {PLoS medicine},\n\tyear = {2008},\n\tvolume = {5},\n\tnumber = {9},\n\tauthor = {Piwowar, H.A. and Becich, M.J. and Bilofsky, H. and Crowley, R.S.}\n}\n\n', 'title': 'Towards a data sharing culture: recommendations for leadership from academic health centers.', 'first_author': u'Piwowar', 'journal': 'PLoS medicine', 'year': '2008', 'number': '9', 'volume': '5', 'first_page': '', 'authors': u'Piwowar, Becich, Bilofsky, Crowley', 'full_citation_type': 'bibtex'}), ('doi', '10.1038/npre.2007.425.2'), ('doi', '10.1038/npre.2007.361'), ('doi', '10.1371/journal.pone.0000308'), ('doi', '10.1371/journal.pone.0000308')]
        assert_items_equal(members, expected)

    def test_extract_members2(self):
        f = open(SAMPLE_EXTRACT_MEMBER_ITEMS_PAGE2, "r")
        members = self.provider._extract_members(f.read(), TEST_ORCID_ID2)
        print members
        expected = [('pmid', '24127438'), ('doi', '10.6084/m9.figshare.790739'), ('doi', '10.6084/m9.figshare.791560'), ('doi', '10.1186/1471-2105-14-158'), ('doi', '10.6084/M9.FIGSHARE.799766'), ('doi', '10.1371/journal.pbio.1001468'), ('doi', '10.7287/PEERJ.PREPRINTS.83'), ('doi', '10.1186/2041-1480-4-34'), ('biblio', {'full_citation': '@article{lapp2012,\n\tvolume  = {28},\n\tnumber  = {3},\n\tpages   = {300-305},\n}\n', 'title': '500,000 fish phenotypes: The new informatics landscape for evolutionary and developmental biology of the vertebrate skeleton', 'first_author': '', 'journal': 'Journal of Applied Ichthyology', 'year': '2012', 'number': '3', 'volume': '28', 'first_page': '300-305', 'authors': '', 'full_citation_type': 'bibtex'}), ('doi', '10.1371/journal.pone.0051070'), ('biblio', {'full_citation': '@article{lapp2012,\n\tvolume  = {61},\n\tnumber  = {4},\n\tpages   = {675-689},\n}\n', 'title': 'NeXML: Rich, extensible, and verifiable representation of comparative data and metadata', 'first_author': '', 'journal': 'Systematic Biology', 'year': '2012', 'number': '4', 'volume': '61', 'first_page': '675-689', 'authors': '', 'full_citation_type': 'bibtex'}), ('doi', '10.4056/sigs.3156511'), ('doi', '10.1371/journal.pcbi.1002799'), ('doi', '10.1002/bult.2011.1720370411'), ('biblio', {'full_citation': '@article{lapp2011,\n\tvolume  = {51},\n\tnumber  = {2},\n\tpages   = {215-223},\n}\n', 'title': 'Overview of FEED, the feeding experiments end-user database', 'first_author': '', 'journal': 'Integrative and Comparative Biology', 'year': '2011', 'number': '2', 'volume': '51', 'first_page': '215-223', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{lapp2011,\n\tvolume  = {2011},\n}\n', 'title': 'The Chado Natural Diversity module: A new generic database schema for large-scale phenotyping and genotyping data', 'first_author': '', 'journal': 'Database', 'year': '2011', 'number': '', 'volume': '2011', 'first_page': '', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': "Midford, P, Mabee, P, Vision, T, Westerfield, M, Midford, P, Balhoff, J, Dahdul, W, Kothari, C, Lapp, H & Lundberg, J, 2010, 'The Teleost Taxonomy Ontology', <i>Nature Precedings</i>.", 'title': 'The Teleost Taxonomy Ontology', 'journal': '', 'year': '2010', 'authors': '', 'full_citation_type': 'formatted_unspecified'}), ('biblio', {'full_citation': "Vos, R, Vos, R, Lapp, H, Piel, W & Tannen, V, 2010, 'TreeBASE2: Rise of the Machines', <i>Nature Precedings</i>.", 'title': 'TreeBASE2: Rise of the Machines', 'journal': '', 'year': '2010', 'authors': '', 'full_citation_type': 'formatted_unspecified'}), ('doi', '10.1371/journal.pone.0010708'), ('doi', '10.4056/sigs/1403501'), ('doi', '10.1371/journal.pone.0010500'), ('doi', '10.1186/2041-1480-1-8'), ('doi', '10.1111/j.2041-210x.2010.00023.x'), ('biblio', {'full_citation': '@article{lapp2010,\n\tvolume  = {59},\n\tnumber  = {4},\n\tpages   = {369-383},\n}\n', 'title': 'The teleost anatomy ontology: Anatomical representation for the genomics age', 'first_author': '', 'journal': 'Systematic Biology', 'year': '2010', 'number': '4', 'volume': '59', 'first_page': '369-383', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': "Midford, P, Midford, P, Mabee, P, Vision, T, Lapp, H, Balhoff, J, Dahdul, W, Kothari, C, Lundberg, J & Westerfield, M, 2009, 'Phenoscape: Ontologies for Large Multi-species Phenotype Datasets', <i>Nature Precedings</i>.", 'title': 'Phenoscape: Ontologies for Large Multi-species Phenotype Datasets', 'journal': '', 'year': '2009', 'authors': '', 'full_citation_type': 'formatted_unspecified'}), ('doi', '10.1111/j.1558-5646.2009.00892.x'), ('biblio', {'full_citation': "O'Meara, B, Rabosky, D, Hipp, A, de Vienne, D, Sidlauskas, B, Hunt, G, Desper, R, Smith, S, Jombart, T, Felsenstein, J, Swofford, D, Kembel, S, Harmon, L, Vision, T, Lapp, H, Waddell, P, Loarie, S, Zanne, A, Maddison, W, Alfaro, M, Zwickl, D, Midford, P, Bell, C, Paradis, E, Orme, D, Bolker, B, Price, S, Heibl, C, Butler, M & Cowan, P, 2008, 'Comparative methods in R hackathon', <i>Nature Precedings</i>.", 'title': 'Comparative methods in R hackathon', 'journal': '', 'year': '2008', 'authors': '', 'full_citation_type': 'formatted_unspecified'}), ('biblio', {'full_citation': u'Lapp, Hilmar, Sendu Bala, James P. Balhoff, Amy Bouck, Naohisa Goto, Mark Holder, Richard Holland, et al. 2007. The 2006 NESCent Phyloinformatics Hackathon: A Field Report. Evolutionary Bioinformatics Online 3: 287\u2013296.', 'title': 'The 2006 NESCent Phyloinformatics Hackathon: A Field Report', 'url': 'http://www.la-press.com/the-2006-nescent-phyloinformatics-hackathon-a-field-report-article-a480', 'journal': '', 'year': '2007', 'authors': '', 'full_citation_type': 'formatted_unspecified'}), ('biblio', {'full_citation': "Lapp, H, 2007, 'Persistent BioPerl', <i>Nature Precedings</i>.", 'title': 'Persistent BioPerl', 'journal': '', 'year': '2007', 'authors': '', 'full_citation_type': 'formatted_unspecified'}), ('doi', '10.1007/s00335-005-0145-5'), ('biblio', {'full_citation': '@article{lapp2006,\n\tvolume  = {7},\n\tnumber  = {3},\n\tpages   = {287-296},\n}\n', 'title': 'Open source tools and toolkits for bioinformatics: Significance, and where are we?', 'first_author': '', 'journal': 'Briefings in Bioinformatics', 'year': '2006', 'number': '3', 'volume': '7', 'first_page': '287-296', 'authors': '', 'full_citation_type': 'bibtex'}), ('doi', '10.1016/s0076-6879(05)03001-6'), ('biblio', {'full_citation': '@article{lapp2005,\n\tvolume  = {16},\n\tnumber  = {8},\n\tpages   = {3847-3864},\n}\n', 'title': 'Large-scale profiling of Rab GTPase trafficking networks: The membrome', 'first_author': '', 'journal': 'Molecular Biology of the Cell', 'year': '2005', 'number': '8', 'volume': '16', 'first_page': '3847-3864', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{lapp2004,\n\tvolume  = {101},\n\tnumber  = {16},\n\tpages   = {6062-6067},\n}\n', 'title': 'A gene atlas of the mouse and human protein-encoding transcriptomes', 'first_author': '', 'journal': 'Proceedings of the National Academy of Sciences of the United States of America', 'year': '2004', 'number': '16', 'volume': '101', 'first_page': '6062-6067', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{lapp2004,\n\tvolume  = {14},\n\tnumber  = {4},\n\tpages   = {742-749},\n}\n', 'title': 'Applications of a rat multiple tissue gene expression data set', 'first_author': '', 'journal': 'Genome Research', 'year': '2004', 'number': '4', 'volume': '14', 'first_page': '742-749', 'authors': '', 'full_citation_type': 'bibtex'}), ('doi', '10.1007/s00138-002-0114-x'), ('biblio', {'full_citation': '@article{lapp2002,\n\tvolume  = {12},\n\tnumber  = {10},\n\tpages   = {1611-1618},\n}\n', 'title': 'The Bioperl toolkit: Perl modules for the life sciences', 'first_author': '', 'journal': 'Genome Research', 'year': '2002', 'number': '10', 'volume': '12', 'first_page': '1611-1618', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{lapp2001,\n\tvolume  = {4266},\n\tpages   = {1-12},\n}\n', 'title': 'A generic and robust approach for the analysis of spot array images', 'first_author': '', 'journal': 'Proceedings of SPIE - The International Society for Optical Engineering', 'year': '2001', 'number': '', 'volume': '4266', 'first_page': '1-12', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{lapp2001,\n\tvolume  = {61},\n\tnumber  = {20},\n\tpages   = {7388-7393},\n}\n', 'title': 'Molecular classification of human carcinomas by use of gene expression signatures', 'first_author': '', 'journal': 'Cancer Research', 'year': '2001', 'number': '20', 'volume': '61', 'first_page': '7388-7393', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{lapp2000,\n\tvolume  = {8},\n\tpages   = {46-56},\n}\n', 'title': 'Robust parametric and semi-parametric spot fitting for spot array images.', 'first_author': '', 'journal': 'Proceedings / . International Conference on Intelligent Systems for Molecular Biology ; ISMB. International Conference on Intelligent Systems for Molecular Biology', 'year': '2000', 'number': '', 'volume': '8', 'first_page': '46-56', 'authors': '', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{lapp2000,\n\tvolume  = {3},\n}\n', 'title': 'Robust spot fitting for genetic spot array images', 'first_author': '', 'journal': 'IEEE International Conference on Image Processing', 'year': '2000', 'number': '', 'volume': '3', 'first_page': '', 'authors': '', 'full_citation_type': 'bibtex'}), ('doi', '10.1007/3-540-48375-6_43')]
        assert_items_equal(members, expected)

    def test_extract_members3(self):
        f = open(SAMPLE_EXTRACT_MEMBER_ITEMS_PAGE3, "r")
        members = self.provider._extract_members(f.read(), TEST_ORCID_ID3)
        print members
        expected = [('biblio', {'isbn': '0702251879', 'title': 'Moving Among Strangers: Randolph Stow and My Family', 'first_author': u'Carey', 'journal': '', 'year': '2013', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey', 'genre': 'book', 'full_citation': '@book{RID:1202132010973-11,\ntitle = {Moving Among Strangers: Randolph Stow and My Family},\npublisher = {},\nyear = {2013},\nauthor = {Carey, Gabrielle},\neditor = {}\n}', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{RID:1202132010973-13,\ntitle = {Randolph Stow: An Ambivalent Australian},\njournal = {Kill Your Darlings},\nyear = {2013},\nauthor = {Carey, Gabrielle},\nnumber = {12},\npages = {27}\n}', 'title': 'Randolph Stow: An Ambivalent Australian', 'first_author': u'Carey', 'journal': 'Kill Your Darlings', 'year': '2013', 'number': '12', 'volume': '', 'first_page': '27', 'authors': u'Carey', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'isbn': '1742759297', 'title': 'Puberty blues', 'first_author': u'Lette', 'journal': '', 'year': '2012', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Lette, Carey', 'genre': 'book', 'full_citation': '@book{RID:1202132010974-1,\ntitle = {Puberty blues},\npublisher = {},\nyear = {2012},\nauthor = {Lette, Kathy and  Carey, Gabrielle},\neditor = {}\n}', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{RID:1202132010974-15,\ntitle = {Moving Among Strangers, Darkly},\njournal = {},\nyear = {2010},\nauthor = {Gabrielle, Carey}\n}', 'title': 'Moving Among Strangers, Darkly', 'first_author': u'Gabrielle', 'journal': '', 'year': '2010', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Gabrielle', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{RID:1202132010974-9,\ntitle = {High-value niche production: what Australian wineries might learn from a Bordeaux first growth},\njournal = {International journal of technology, policy and management},\nyear = {2009},\nauthor = {Aylward, David and  Carey, Gabrielle},\nvolume = {9},\nnumber = {4},\npages = {342-357}\n}', 'title': 'High-value niche production: what Australian wineries might learn from a Bordeaux first growth', 'first_author': u'Aylward', 'journal': 'International journal of technology, policy and management', 'year': '2009', 'number': '4', 'volume': '9', 'first_page': '342-357', 'authors': u'Aylward, Carey', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'isbn': '1921372621', 'title': 'Waiting Room: A Memoir', 'first_author': u'Carey', 'journal': '', 'year': '2009', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey', 'genre': 'book', 'full_citation': '@book{RID:1202132010974-12,\ntitle = {Waiting Room: A Memoir},\npublisher = {},\nyear = {2009},\nauthor = {Carey, Gabrielle},\neditor = {}\n}', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{RID:1202132010974-10,\ntitle = {Literature and Religion as Rivals},\njournal = {Sydney Studies in Religion},\nyear = {2008},\nauthor = {Carey, Gabrielle}\n}', 'title': 'Literature and Religion as Rivals', 'first_author': u'Carey', 'journal': 'Sydney Studies in Religion', 'year': '2008', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('doi', '10.1162/daed.2006.135.4.60'), ('biblio', {'isbn': '0733305741', 'title': 'Australian Story: Australian Lives', 'first_author': u'Carey', 'journal': '', 'year': '1997', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey', 'genre': 'book', 'full_citation': '@book{RID:1202132010974-7,\ntitle = {Australian Story: Australian Lives},\npublisher = {},\nyear = {1997},\nauthor = {Carey, Gabrielle},\neditor = {}\n}', 'full_citation_type': 'bibtex'}), ('biblio', {'isbn': '0140259384', 'title': 'The Penguin Book of Death', 'first_author': u'Carey', 'journal': '', 'year': '1997', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey, Sorensen', 'genre': 'book', 'full_citation': '@book{RID:1202132010975-8,\ntitle = {The Penguin Book of Death},\npublisher = {},\nyear = {1997},\nauthor = {Carey, Gabrielle and  Sorensen, Rosemary Lee},\neditor = {}\n}', 'full_citation_type': 'bibtex'}), ('biblio', {'full_citation': '@article{RID:1202132010975-6,\ntitle = {Prenatal Depression, Postmodern World},\njournal = {Mother love: stories about births, babies & beyond},\nyear = {1996},\nauthor = {Carey, Gabrielle},\npages = {179}\n}', 'title': 'Prenatal Depression, Postmodern World', 'first_author': u'Carey', 'journal': 'Mother love: stories about births, babies & beyond', 'year': '1996', 'number': '', 'volume': '', 'first_page': '179', 'authors': u'Carey', 'genre': 'journal article', 'full_citation_type': 'bibtex'}), ('biblio', {'isbn': '0330355988', 'title': 'The Borrowed Girl', 'first_author': u'Carey', 'journal': '', 'year': '1994', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey', 'genre': 'book', 'full_citation': '@book{RID:1202132010975-5,\ntitle = {The Borrowed Girl},\npublisher = {},\nyear = {1994},\nauthor = {Carey, Gabrielle},\neditor = {}\n}', 'full_citation_type': 'bibtex'}), ('biblio', {'isbn': '0330272942', 'title': "In My Father's House", 'first_author': u'Carey', 'journal': '', 'year': '1992', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey, Hudson', 'genre': 'book', 'full_citation': "@book{RID:1202132010975-4,\ntitle = {In My Father's House},\npublisher = {},\nyear = {1992},\nauthor = {Carey, Gabrielle and  Hudson, Elaine},\neditor = {}\n}", 'full_citation_type': 'bibtex'}), ('biblio', {'isbn': '0140074252', 'title': 'Just Us', 'first_author': u'Carey', 'journal': '', 'year': '1984', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey', 'genre': 'book', 'full_citation': '@book{RID:1202132010975-3,\ntitle = {Just Us},\npublisher = {},\nyear = {1984},\nauthor = {Carey, Gabrielle},\neditor = {}\n}', 'full_citation_type': 'bibtex'}), ('biblio', {'isbn': '0872237680', 'title': 'Puberty blues', 'first_author': u'Carey', 'journal': '', 'year': '1982', 'number': '', 'volume': '', 'first_page': '', 'authors': u'Carey, Lette', 'genre': 'book', 'full_citation': '@book{RID:1202132010975-2,\ntitle = {Puberty blues},\npublisher = {},\nyear = {1982},\nauthor = {Carey, Gabrielle and  Lette, Kathy},\neditor = {}\n}', 'full_citation_type': 'bibtex'})]
        print expected
        assert_items_equal(members, expected)


    def test_extract_members_zero_items(self):
        page = """{"message-version":"1.0.6","orcid-profile":{"orcid":{"value":"0000-0003-1613-5981"}}}"""
        members = self.provider._extract_members(page, TEST_ORCID_ID)
        assert_equals(members, [])

    @http
    def test_member_items(self):
        members = self.provider.member_items(TEST_ORCID_ID)
        print members
        expected = [('doi', '10.1002/meet.14504701413'), ('doi', '10.1038/npre.2007.425.2'), ('doi', '10.1002/meet.14504701421'), ('doi', '10.1038/npre.2008.2152.1'), ('doi', '10.1038/npre.2007.361'), ('doi', '10.1038/473285a'), ('doi', '10.1038/npre.2010.4267.1'), ('doi', '10.1016/j.joi.2009.11.010'), ('doi', '10.1038/npre.2010.5452.1')]
        assert len(members) >= len(expected), str(members)

    @http
    def test_member_items_url_format(self):
        members = self.provider.member_items("http://orcid.org/" + TEST_ORCID_ID)
        print members
        expected = [('doi', '10.1002/meet.14504701413'), ('doi', '10.1038/npre.2007.425.2'), ('doi', '10.1002/meet.14504701421'), ('doi', '10.1038/npre.2008.2152.1'), ('doi', '10.1038/npre.2007.361'), ('doi', '10.1038/473285a'), ('doi', '10.1038/npre.2010.4267.1'), ('doi', '10.1016/j.joi.2009.11.010'), ('doi', '10.1038/npre.2010.5452.1')]
        assert len(members) >= len(expected), str(members)

    @http
    def test_member_items_some_missing_dois(self):
        members = self.provider.member_items("0000-0001-5109-3700")  #another.  some don't have dois
        print members
        expected = [('doi', u'10.1087/20120404'), ('doi', u'10.1093/scipol/scs030'), ('doi', u'10.1126/science.caredit.a1200080'), ('doi', u'10.1016/S0896-6273(02)01067-X'), ('doi', u'10.1111/j.1469-7793.2000.t01-2-00019.xm'), ('doi', u'10.1046/j.0022-3042.2001.00727.x'), ('doi', u'10.1097/ACM.0b013e31826d726b'), ('doi', u'10.1126/science.1221840'), ('doi', u'10.1016/j.brainresbull.2006.08.006'), ('doi', u'10.1016/0006-8993(91)91536-A'), ('doi', u'10.1076/jhin.11.1.70.9111'), ('doi', u'10.2139/ssrn.1677993')]
        assert len(members) >= len(expected), str(members)


    @http
    def test_member_items_mla_format(self):
        members = self.provider.member_items("http://orcid.org/" + "0000-0002-3878-917X")
        print members
        expected = "hi"
        assert len(members) >= len(expected), str(members)


