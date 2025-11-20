package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;


public enum AssignmentMasterStatus {
	MASTER_NEW, MASTER_WORKING, MASTER_WORKED_NOT_VIEWED, MASTER_WORKED_VIEWED, MASTER_REJECTED;
	
	public String getTranslation(){
		return switch (this) {
			case MASTER_NEW -> "NUOVO";
			case MASTER_WORKING -> "IN LAVORAZIONE";
			case MASTER_WORKED_NOT_VIEWED -> "LAVORATO E NON VISIONATO";
			case MASTER_WORKED_VIEWED -> "LAVORATO E VISIONATO";
			case MASTER_REJECTED -> "RIFIUTATO";
		};
	}
}
