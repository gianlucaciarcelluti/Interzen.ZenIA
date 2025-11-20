package it.interzen.zencommonlibrary.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PagedResponseDTO<T> {
    private List<T> content;
    private long totalElements;
    private int page;
    private int size;
}