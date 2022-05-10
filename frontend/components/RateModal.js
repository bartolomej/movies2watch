import {Button, Loading, Modal, Text} from "@nextui-org/react";
import RateInput from "./RateInput";
import {useState} from "react";

export default function RateModal({ open, submitting, onSubmit, onClose }) {
    const [rating, setRating] = useState(0);

    return (
        <Modal
            closeButton
            aria-labelledby="modal-title"
            open={open}
            onClose={onClose}
        >
            <Modal.Header>
                <Text id="modal-title" size={18}>
                    Rate this movie
                </Text>
            </Modal.Header>
            <Modal.Body style={{display: 'flex', alignItems: 'center'}}>
                <RateInput initialRating={rating} onChange={setRating}/>
            </Modal.Body>
            <Modal.Footer>
                <Button auto onClick={() => {
                    onSubmit(rating);
                    setRating(0)
                }}>
                    {submitting ? <Loading color="currentColor" size="sm" /> : 'Submit'}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}