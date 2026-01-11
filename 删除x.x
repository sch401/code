Sub CleanHeading2ManualXDotX_KeepNumbering()
    Dim para As Paragraph
    Dim r As Range
    Dim txt As String
    Dim reg As Object
    
    Set reg = CreateObject("VBScript.RegExp")
    reg.Pattern = "^\d+\.\d+[ \t]*"   ' 匹配 1.1、12.5 等开头 + 空格/制表符
    reg.Global = False
    reg.IgnoreCase = True
    
    For Each para In ActiveDocument.Paragraphs
        ' 仅处理 标题 2 样式
        If para.Style = ActiveDocument.Styles("标题 2") Then
            ' 仅处理已有多级编号的段落（避免误删纯文本标题）
            If para.Range.ListFormat.ListType <> wdListNoNumbering Then
                Set r = para.Range
                r.End = r.End - 1       ' 去掉段落标记 (vbCr)
                txt = r.Text
            
                If reg.Test(txt) Then
                    txt = reg.Replace(txt, "")
                    txt = LTrim(txt)    ' 清除可能残留的前导空格
                    r.Text = txt
                End If
            End If
        End If
    Next para
    
    MsgBox "标题 2 中手动输入的 X.X 编号已清理，多级列表编号已保留。", vbInformation
End Sub
