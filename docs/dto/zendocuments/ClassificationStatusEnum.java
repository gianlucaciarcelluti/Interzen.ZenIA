package it.interzen.zencommonlibrary.dto.zendocuments;

public enum ClassificationStatusEnum {
    CURRENT(1, "Current"),
    INVALID(2, "Invalid");

    int id;
    String description;

    ClassificationStatusEnum(int id, String description) {
        this.id = id;
        this.description = description;
    }
}
