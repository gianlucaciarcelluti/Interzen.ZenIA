package it.interzen.zencommonlibrary.dto.zenmailroom;

public enum SendingLogStatusEnum {
	NONE,
	ERROR_SENT,
	ACCEPTANCE_WAITING,
	ACCEPTANCE_KO,
	DELIVERY_WAITING,
	DELIVERY_PARTIAL,
	DELIVERY_ERROR,
	COMPLETED;
}
