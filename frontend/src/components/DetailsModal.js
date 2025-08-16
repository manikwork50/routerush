import React from 'react';
import Modal from "react-modal";

export default function DetailsModal({ isOpen, details, onClose }) {
  return (
    <Modal isOpen={isOpen} onRequestClose={onClose} contentLabel="Route Details">
      <h3>🛣️ Travel Details</h3>
      <div>{details ? <div dangerouslySetInnerHTML={{__html:details}} /> : null}</div>
      <button onClick={onClose}>Close</button>
    </Modal>
  );
}

