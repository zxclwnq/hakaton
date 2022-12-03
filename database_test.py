# Добавление в БД рандомных значений для проверки

from data.proposals import Proposal
from data import db_session
from tables import user_data_empty,evaluation_table_text_default,lowering_criteria_default,evaluation_table_video_default

propose_id = 264
def add(db_ses):
    new_proposal = Proposal()
    new_proposal.make_proposal(propose_id, "text", "https://it.orb.ru/hackathon",
                               user_data_empty)
    db_ses.add(new_proposal)
    db_ses.commit()

def approve(db_ses):
    propose = db_ses.query(Proposal).filter(Proposal.id == propose_id).first()
    if propose.type == 'text':
        propose.verify_proposal(evaluation_table_text_default,
                                lowering_criteria_default,
                                "verified")
    else:
        propose.verify_proposal(evaluation_table_video_default,
                                lowering_criteria_default,
                                "verified")
    db_ses.commit()
def main():
    db_session.global_init("main.db")
    db_ses = db_session.create_session()
    #add(db_ses)
    approve(db_ses)


if __name__ == '__main__':
    main()