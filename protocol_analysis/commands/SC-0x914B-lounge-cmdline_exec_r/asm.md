# 汇编证据 —— SC-0x914B-lounge-cmdline_exec_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB9` @ `B6C29E`）

```asm
; VA: B6C29E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xB9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6C2DF`、`B6C3BC`
; 字段 2 —— res：偏移 4，长度 L+1，线类型 string（命令行执行结果文本（日志串 `res='...'`；NUL 结尾））
;   `B6C313`、`B6C3E4`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6C33C
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x5A）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6C44D —— `vt[0x130]`（2 实参）
```
